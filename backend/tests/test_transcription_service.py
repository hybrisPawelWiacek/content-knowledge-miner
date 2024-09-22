# backend/tests/test_transcription_service.py

import unittest
from services.transcription_service import transcribe_audio

class TestTranscriptionService(unittest.TestCase):

    def test_transcribe_audio(self):
        # Since transcribing requires an actual audio file,
        # you might use a small test audio file stored in a test directory.
        audio_file_path = 'tests/test_audio.wav'
        transcription = transcribe_audio(audio_file_path)
        self.assertIsInstance(transcription, str)
        self.assertTrue(len(transcription) > 0)

if __name__ == '__main__':
    unittest.main()
