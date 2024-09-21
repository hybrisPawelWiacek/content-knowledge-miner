# /backend/services/airtable_service.py

import os
from airtable import Airtable
from config import Config
from datetime import datetime
from models import VideoMetadata, Summary

AIRTABLE_API_KEY = Config.AIRTABLE_API_KEY
AIRTABLE_BASE_ID = Config.AIRTABLE_BASE_ID

videos_table = Airtable(AIRTABLE_BASE_ID, 'Videos', AIRTABLE_API_KEY)
user_inputs_table = Airtable(AIRTABLE_BASE_ID, 'UserInputs', AIRTABLE_API_KEY)
summaries_table = Airtable(AIRTABLE_BASE_ID, 'Summaries', AIRTABLE_API_KEY)

def get_user_inputs(video_id):
    """
    Retrieves user-provided inputs for a specific video from the UserInputs table.
    """
    records = user_inputs_table.get_all(
        view='Grid view',
        formula=f"{{Video ID}} = '{video_id}'"
    )
    return records

def save_video_data(video_metadata: VideoMetadata):
    """
    Saves or updates video data in the Videos table.
    """
    # Prepare data in Airtable format
    airtable_fields = video_metadata.to_airtable_fields()
    # Check if the video already exists
    records = videos_table.get_all(
        view='Grid view',
        formula=f"{{Video ID}} = '{video_metadata.video_id}'"
    )
    if records:
        # Update existing record
        record_id = records[0]['id']
        videos_table.update(record_id, airtable_fields)
    else:
        # Create new record
        videos_table.insert(airtable_fields)
# /backend/services/airtable_service.py

def save_summary(summary: Summary):
    # First, we need to get the record ID for the video
    video_records = videos_table.get_all(
        formula=f"{{Video ID}} = '{summary.video_id}'"
    )
    
    if not video_records:
        raise ValueError(f"No video found with ID {summary.video_id}")

    video_record_id = video_records[0]['id']

    # Prepare data in Airtable format
    airtable_fields = {
        'Video ID': [video_record_id],  # This should be an array with one record ID
        'Summary Text': summary.summary_text,
        'Key Topics': ', '.join(summary.key_topics)  # Assuming this is a text field, not a linked record
    }

    # Check if the summary already exists
    records = summaries_table.get_all(
        view='Grid view',
        formula=f"RECORD_ID({{Video ID}}) = '{video_record_id}'"
    )

    if records:
        record_id = records[0]['id']
        summaries_table.update(record_id, airtable_fields)
    else:
        summaries_table.insert(airtable_fields)
