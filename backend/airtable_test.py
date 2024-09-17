# /backend/airtable_test.py

import os
from airtable import Airtable
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

# Initialize Airtable client for the Videos table
airtable_videos = Airtable(AIRTABLE_BASE_ID, 'Videos', AIRTABLE_API_KEY)

# Fetch all records from the Videos table
records = airtable_videos.get_all()

print(f"Retrieved {len(records)} records from the Videos table.")
