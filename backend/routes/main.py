# /backend/routes/main.py

from flask import Blueprint, request, jsonify
from services.youtube_service import get_video_id, get_video_metadata, check_captions_available, download_audio, get_caption_track, get_captions_pytube
from services.transcription_service import transcribe_audio
from services.airtable_service import get_user_inputs, save_video_data
import os
from datetime import datetime
from models.models import VideoMetadata, UserInput

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
            # Fetch captions and use them as transcription
            transcription = get_caption_track(video_id)
            print(f"Transcription from captions: {transcription}")
            if not transcription:
                transcription = get_captions_pytube(video_url)
            if not transcription:
                transcription = 'Failed to retrieve captions.'
        
        if transcription == 'Failed to retrieve captions.':
            print("Transcription from captions failed, trying audio transcription.")
            try:
                # Download audio and perform transcription
                audio_file_path = download_audio(video_url, output_path='downloads/')
                print(f"Audio file path: {audio_file_path}")
                if audio_file_path:
                    transcription = transcribe_audio(audio_file_path)
                    print(f"Transcription from audio: {transcription}")
                    # Delete the audio file after transcription
                    os.remove(audio_file_path)
                else:
                    transcription = 'Audio download failed. Please try again.'
            except Exception as e:
                print(f"Error during audio download: {str(e)}")
                transcription = f'Audio download failed: {str(e)}'

        # Update the transcript_text field in metadata
        metadata.transcript_text = transcription

        # Get user inputs
        user_input_records = get_user_inputs(video_id)
        user_inputs = []
        for record in user_input_records:
            fields = record.get('fields', {})
            user_input = UserInput(
                video_id=video_id,
                category=fields.get('Category'),
                comments=fields.get('Comments'),
                highlights=fields.get('Highlights'),
                quality_rating=fields.get('Quality Rating')
            )
            user_inputs.append(user_input)

        # Save video data to Airtable
        save_video_data(metadata)

        # Prepare response data
        response = {
            'video_id': video_id,
            'metadata': metadata.__dict__,
            'user_inputs': [ui.__dict__ for ui in user_inputs]
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
