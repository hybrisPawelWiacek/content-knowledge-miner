# /backend/services/youtube_service.py

import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pytube import YouTube
from config import Config

YOUTUBE_API_KEY = Config.YOUTUBE_API_KEY

def get_video_id(video_url):
    """
    Extracts the video ID from a YouTube URL.
    """
    if "v=" in video_url:
        return video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
        return video_url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")

def get_video_metadata(video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        request = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=video_id
        )
        response = request.execute()
        if response['items']:
            return response['items'][0]
        else:
            raise ValueError("No video found with the provided ID")
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return None

def check_captions_available(video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        request = youtube.captions().list(
            part='id',
            videoId=video_id
        )
        response = request.execute()
        return len(response.get('items', [])) > 0
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return False

def download_audio(video_url, output_path='downloads/'):
    """
    Downloads the audio of a YouTube video and converts it to WAV format.
    """
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
        return wav_file
    except Exception as e:
        print(f"An error occurred while downloading audio: {e}")
        return None
