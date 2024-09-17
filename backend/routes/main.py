# /backend/routes/main.py

from flask import Blueprint, request, jsonify
from services.youtube_service import get_video_id, get_video_metadata, check_captions_available, download_audio
from services.transcription_service import transcribe_audio
from services.airtable_service import get_user_inputs, save_video_data
import os
from datetime import datetime  # Add this import

main = Blueprint('main', __name__)

@main.route('/process_video', methods=['POST'])
def process_video():
    data = request.get_json()
    video_url = data.get('video_url')

    try:
        video_id = get_video_id(video_url)
        metadata = get_video_metadata(video_id)
        captions_available = check_captions_available(video_id)

        if captions_available:
            # TODO: Fetch captions and use them as transcription
            transcription = 'Captions are available but fetching captions is not yet implemented.'
        else:
            # Download audio and perform transcription
            audio_file_path = download_audio(video_url, output_path='downloads/')
            if audio_file_path:
                transcription = transcribe_audio(audio_file_path)
                # Delete the audio file after transcription
                os.remove(audio_file_path)
            else:
                transcription = 'Audio download failed.'

        # Get user inputs from Airtable
        user_inputs = get_user_inputs(video_id)

        # Prepare data to save to Airtable
        video_data = {
            'Video ID': video_id,
            'Title': metadata['snippet']['title'],
            'Description': metadata['snippet']['description'],
            'Transcript Text': transcription,
            # Add other fields as needed
            'Published At': datetime.strptime(metadata['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%m/%d/%Y'),
            'Duration': metadata['contentDetails']['duration'],
            'View Count': int(metadata['statistics'].get('viewCount', 0)),
            'Like Count': int(metadata['statistics'].get('likeCount', 0)),
            'Comment Count': int(metadata['statistics'].get('commentCount', 0)),
        }

        # Save video data to Airtable
        save_video_data(video_data)

        # For now, return the metadata, transcription, and user inputs
        response = {
            'video_id': video_id,
            'metadata': metadata,
            'transcription': transcription,
            'user_inputs': user_inputs
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
