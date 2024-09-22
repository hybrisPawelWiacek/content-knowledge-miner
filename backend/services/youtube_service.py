# /backend/services/youtube_service.py

import os
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
import xml.etree.ElementTree as ET
from pytube import YouTube
from config import Config
from pydub import AudioSegment
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
from models.models import VideoMetadata
import isodate

logger = logging.getLogger(__name__)

YOUTUBE_API_KEY = Config.YOUTUBE_API_KEY
#
# # Set up the OAuth 2.0 flow
# flow = Flow.from_client_secrets_file(
#     'path/to/your/client_secrets.json',
#     scopes=['https://www.googleapis.com/auth/youtube.force-ssl']
# )

# # Prompt the user to go through the OAuth flow
# flow.run_local_server(port=8080, prompt='consent')

# # Get the credentials
# credentials = flow.credentials

# def get_caption_track_oauth(video_id, language='en'):
#     try:
#         # Build the YouTube API client with the OAuth 2.0 credentials
#         youtube = build('youtube', 'v3', credentials=credentials)
        
#         request = youtube.captions().list(
#             part='snippet',
#             videoId=video_id
#         )
#         response = request.execute()
#         caption_id = None
#         for item in response.get('items', []):
#             if item['snippet']['language'] == language:
#                 caption_id = item['id']
#                 break
        
#         if caption_id:
#             # Download the caption track
#             request = youtube.captions().download(
#                 id=caption_id,
#                 tfmt='ttml'
#             )
#             caption_data = request.execute()
            
#             # Process the TTML data (you'll need to implement ttml_to_text function)
#             transcript = ttml_to_text(caption_data)
#             return transcript
#         else:
#             return None
#     except HttpError as e:
#         logger.error(f"An HTTP error occurred: {e}")
#         return None
#

def get_video_id(video_url):
    """
    Extracts the video ID from a YouTube URL.
    """
    logger.info(f"Extracting video ID from URL: {video_url}")
    if "v=" in video_url:
        return video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
        return video_url.split("youtu.be/")[1].split("?")[0]
    else:
        logger.error(f"Invalid YouTube URL: {video_url}")
        raise ValueError("Invalid YouTube URL")

def get_video_metadata(video_id):
    logger.info(f"Fetching metadata for video ID: {video_id}")
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        request = youtube.videos().list(
            part = 'snippet,contentDetails,statistics,status,topicDetails,recordingDetails,liveStreamingDetails,localizations,player',
            id=video_id
        )
        response = request.execute()
        if response['items']:
            item = response['items'][0]

            # Parse duration
            duration_iso = item['contentDetails']['duration']
            duration = isodate.parse_duration(duration_iso)
            duration_str = str(duration)

            metadata = VideoMetadata(
                video_id=video_id,
                title=item['snippet']['title'],
                description=item['snippet']['description'],
                published_at=item['snippet']['publishedAt'],
                duration=duration_str,
                view_count=int(item['statistics'].get('viewCount', 0)),
                like_count=int(item['statistics'].get('likeCount', 0)),
                comment_count=int(item['statistics'].get('commentCount', 0)),
                transcript_text='',  # Will be filled later
                key_topics=[],  
                raw_data=item
            )

            logger.info(f"Successfully fetched metadata for video ID: {video_id}")
            return metadata
        else:
            logger.warning(f"No video found with the provided ID: {video_id}")
            raise ValueError("No video found with the provided ID")
    except HttpError as e:
        logger.error(f"An HTTP error occurred while fetching metadata for video ID {video_id}: {e}")
        return None

def check_captions_available(video_id):
    logger.info(f"Checking captions availability for video ID: {video_id}")
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        request = youtube.captions().list(
            part='id',
            videoId=video_id
        )
        response = request.execute()
        captions_available = len(response.get('items', [])) > 0
        logger.info(f"Captions available for video ID {video_id}: {captions_available}")
        return captions_available
    except HttpError as e:
        logger.error(f"An HTTP error occurred while checking captions for video ID {video_id}: {e}")
        return False

def download_audio(video_url, output_path='downloads/'):
    """
    Downloads the audio of a YouTube video and converts it to WAV format.
    """
    logger.info(f"Downloading audio for video URL: {video_url}")
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        temp_file = audio_stream.download(output_path=output_path)
        # Convert to WAV format
        base, ext = os.path.splitext(temp_file)
        wav_file = f"{base}.wav"
        AudioSegment.from_file(temp_file).export(wav_file, format='wav')
        os.remove(temp_file)  # Remove the original file
        logger.info(f"Successfully downloaded and converted audio for video URL: {video_url}")
        return wav_file
    except Exception as e:
        logger.error(f"An error occurred while downloading audio for video URL {video_url}: {e}")
        return None

def get_caption_track(video_id, language='en'):
    logger.info(f"Fetching caption track for video ID: {video_id}, language: {language}")
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        request = youtube.captions().list(
            part='snippet',
            videoId=video_id
        )
        response = request.execute()
        caption_id = None
        for item in response.get('items', []):
            if item['snippet']['language'] == language:
                caption_id = item['id']
                break
        if caption_id:
            # Obtain the caption download URL
            caption_download_url = f"https://www.googleapis.com/youtube/v3/captions/{caption_id}?tfmt=ttml&key={YOUTUBE_API_KEY}"
            headers = {'Authorization': f'Bearer {YOUTUBE_API_KEY}'}
            caption_response = requests.get(caption_download_url, headers=headers)
            if caption_response.status_code == 200:
                ttml_data = caption_response.text
                transcript = ttml_to_text(ttml_data)
                logger.info(f"Successfully fetched and processed caption track for video ID: {video_id}")
                return transcript
            else:
                logger.warning(f"Failed to download captions for video ID {video_id}: {caption_response.status_code}")
                return None
        else:
            logger.warning(f"No caption track found for video ID {video_id} in language {language}")
            return None
    except HttpError as e:
        logger.error(f"An HTTP error occurred while fetching caption track for video ID {video_id}: {e}")
        return None
    
def get_captions_pytube(video_url, language='en'):
    logger.info(f"Fetching captions using pytube for video URL: {video_url}, language: {language}")
    try:
        yt = YouTube(video_url)
        caption = yt.captions.get_by_language_code(language)
        if caption:
            srt_data = caption.generate_srt_captions()
            transcript = srt_to_text(srt_data)
            logger.info(f"Successfully fetched and processed captions for video URL: {video_url}")
            return transcript
        else:
            logger.warning(f"No captions found for video URL {video_url} in language {language}")
            return None
    except Exception as e:
        logger.error(f"An error occurred while fetching captions for video URL {video_url}: {e}")
        return None
    
def ttml_to_text(ttml_data):
    logger.info("Converting TTML data to text")
    # Parse TTML (XML) and extract text
    root = ET.fromstring(ttml_data)
    namespaces = {'tt': 'http://www.w3.org/ns/ttml'}
    texts = []
    for p in root.findall('.//tt:p', namespaces):
        texts.append(p.text)
    return ' '.join(texts)

def srt_to_text(srt_data):
    logger.info("Converting SRT data to text")
    lines = srt_data.split('\n')
    return ' '.join(line for line in lines if not line.isdigit() and not '-->' in line and line.strip())
