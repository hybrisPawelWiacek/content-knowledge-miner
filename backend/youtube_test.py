# /backend/youtube_test.py

import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Test with a known video ID
video_id = '2NSIaWo2vkY'  # Example video ID

request = youtube.videos().list(
    part='snippet,contentDetails,statistics',
    id=video_id
)
response = request.execute()

print(response)
#python youtube_test.py