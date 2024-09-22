# backend/tests/test_youtube_service.py

import unittest
from services.youtube_service import get_video_id, get_video_metadata

class TestYouTubeService(unittest.TestCase):

    def test_get_video_id(self):
        url = 'https://www.youtube.com/watch?v=7Jo9D6BkAJU'
        expected_video_id = 'dQw4w9WgXcQ'
        self.assertEqual(get_video_id(url), expected_video_id)

    def test_get_video_metadata(self):
        video_id = 'dQw4w9WgXcQ'
        metadata = get_video_metadata(video_id)
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata.video_id, video_id)

if __name__ == '__main__':
    unittest.main()
