# /backend/services/airtable_service.py

import os
from airtable import Airtable
from config import Config
from datetime import datetime
from models import VideoMetadata, Summary
import logging

logger = logging.getLogger(__name__)

AIRTABLE_API_KEY = Config.AIRTABLE_API_KEY
AIRTABLE_BASE_ID = Config.AIRTABLE_BASE_ID

videos_table = Airtable(AIRTABLE_BASE_ID, 'Videos', AIRTABLE_API_KEY)
user_inputs_table = Airtable(AIRTABLE_BASE_ID, 'UserInputs', AIRTABLE_API_KEY)
summaries_table = Airtable(AIRTABLE_BASE_ID, 'Summaries', AIRTABLE_API_KEY)

def get_user_inputs(video_id):
    """
    Retrieves user-provided inputs for a specific video from the UserInputs table.
    """
    logger.info(f"Fetching user inputs for video ID: {video_id}")
    records = user_inputs_table.get_all(
        view='Grid view',
        formula=f"{{Video ID}} = '{video_id}'"
    )
    logger.info(f"Found {len(records)} user input records for video ID: {video_id}")
    return records

def save_video_data(video_metadata: VideoMetadata):
    """
    Saves or updates video data in the Videos table.
    """
    logger.info(f"Saving video data for video ID: {video_metadata.video_id}")
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
        logger.info(f"Updating existing record for video ID: {video_metadata.video_id}")
        videos_table.update(record_id, airtable_fields)
    else:
        # Create new record
        logger.info(f"Creating new record for video ID: {video_metadata.video_id}")
        videos_table.insert(airtable_fields)
# /backend/services/airtable_service.py

def save_summary(summary: Summary):
    logger.info(f"Saving summary for video ID: {summary.video_id}")
    
    # First, we need to get the record ID for the video
    video_records = videos_table.get_all(
        formula=f"{{Video ID}} = '{summary.video_id}'"
    )
    
    if not video_records:
        logger.error(f"No video found with ID {summary.video_id}")
        raise ValueError(f"No video found with ID {summary.video_id}")

    video_record_id = video_records[0]['id']

    # Prepare data in Airtable format
    airtable_fields = summary.to_airtable_fields()
    
    # Ensure 'Video ID' is always an array of record IDs
    airtable_fields['Video ID'] = [video_record_id]

    # Check if the summary already exists
    existing_summary = summaries_table.get_all(
        view='Grid view',
        formula=f"{{Video ID}} = '{summary.video_id}'"
    )
    logger.info(f"Existing summary for video ID {summary.video_id}: {existing_summary}")

    if existing_summary:
        record_id = existing_summary[0]['id']
        logger.info(f"Updating existing summary with record ID: {record_id}")
        summaries_table.update(record_id, airtable_fields)
    else:
        logger.info(f"Creating new summary for video ID: {summary.video_id}")
        summaries_table.create(airtable_fields)

    # Verify the operation
    updated_summary = summaries_table.get_all(
        view='Grid view',
        formula=f"{{Video ID}} = '{summary.video_id}'"
    )
    logger.info(f"Updated/Created summary: {updated_summary}")
