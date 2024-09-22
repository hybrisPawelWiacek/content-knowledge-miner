# /backend/services/transcription_service.py

import os
from google.cloud import speech_v1p1beta1 as speech
from config import Config
import io
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Ensure that the GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# This should point to the path of your service account JSON key file

def transcribe_audio(file_path):
    """
    Transcribes the audio file at the specified path using Google Cloud Speech-to-Text.
    """
    logger.info(f"Starting transcription for audio file: {file_path}")
    try:
        # Instantiate a client
        client = speech.SpeechClient()
        logger.debug("Speech client instantiated")

        # Loads the audio into memory
        with io.open(file_path, 'rb') as audio_file:
            content = audio_file.read()
        logger.debug("Audio file loaded into memory")

        audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US',  # Change this if needed
            enable_automatic_punctuation=True,
            model='video',  # Options: 'video', 'phone_call', 'default', etc.
        )
        logger.debug("Recognition config set up")

        # Detects speech in the audio file
        logger.info("Sending request to Google Cloud Speech-to-Text API")
        response = client.recognize(config=config, audio=audio)

        # Concatenate the transcribed text
        transcription = ''
        for result in response.results:
            transcription += result.alternatives[0].transcript + ' '

        logger.info("Transcription completed successfully")
        return transcription.strip()
    except Exception as e:
        logger.error(f"An error occurred during transcription: {e}")
        return ''
