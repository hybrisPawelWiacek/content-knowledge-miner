# /backend/routes/main.py

from flask import Blueprint, request, jsonify
from services.youtube_service import get_video_id, get_video_metadata, check_captions_available, download_audio, get_caption_track, get_captions_pytube
from services.transcription_service import transcribe_audio
from services.airtable_service import get_user_inputs, save_video_data, save_summary
import os
from datetime import datetime
from models.models import VideoMetadata, UserInput, Summary
from services.llm_service import generate_summary
import logging

logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

@main.route('/process_video', methods=['POST', 'OPTIONS'])
def process_video():
    if request.method == 'OPTIONS':
        return '', 204
    logger.info("Processing video request received")
    data = request.get_json()
    video_url = data.get('video_url')
    model_choice = data.get('model', 'gpt-4o-mini')
    logger.info(f"Model choice fetched from frontend: {model_choice}")

    try:
        logger.info(f"Processing video URL: {video_url}")
        video_id = get_video_id(video_url)
        metadata = get_video_metadata(video_id)
        captions_available = check_captions_available(video_id)

        if captions_available:
            logger.info("Captions available, fetching transcription")
            transcription = get_caption_track(video_id)
            logger.debug(f"Transcription from captions: {transcription}")
            if not transcription:
                logger.info("Attempting to get captions using pytube")
                transcription = get_captions_pytube(video_url)
            if not transcription:
                logger.warning("Failed to retrieve captions")
                transcription = 'Failed to retrieve captions.'
        
        if transcription == 'Failed to retrieve captions.':
            logger.info("Transcription from captions failed, attempting audio transcription")
            try:
                audio_file_path = download_audio(video_url, output_path='downloads/')
                logger.info(f"Audio file downloaded: {audio_file_path}")
                if audio_file_path:
                    transcription = transcribe_audio(audio_file_path)
                    logger.debug(f"Transcription from audio: {transcription}")
                    os.remove(audio_file_path)
                    logger.info("Audio file deleted after transcription")
                else:
                    logger.error("Audio download failed")
                    transcription = 'Audio download failed. Please try again.'
            except Exception as e:
                logger.error(f"Error during audio download: {str(e)}")
                transcription = f'Audio download failed: {str(e)}'

        metadata.transcript_text = transcription

        logger.info("Fetching user inputs")
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

        logger.info("Saving video data to Airtable")
        save_video_data(metadata)

        logger.info("Generating summary")
        prompt = f"Please provide a professional summary of the following content:\n\n{metadata.transcript_text}\n\nSummary should be around 500 words, include key points, and be formatted as formatted text."
        summary_text = generate_summary(prompt, model=model_choice)

        summary = Summary(
            video_id=video_id,
            summary_text=summary_text,
            key_topics=[]
        )

        logger.info("Saving summary")
        save_summary(summary)

        response = {
            'video_id': video_id,
            'metadata': metadata.__dict__,
            'user_inputs': [ui.__dict__ for ui in user_inputs],
            'summary': summary.__dict__
        }

        logger.info("Video processing completed successfully")
        return jsonify(response)
    except Exception as e:
        logger.exception("An error occurred while processing the video.")
        return jsonify({'error': str(e)}), 500

@main.route('/test', methods=['GET', 'OPTIONS'])
def test_route():
    print("Headers:", dict(request.headers))
    print("Method:", request.method)
    print("Args:", request.args)
    return jsonify({"message": "Test successful"})
