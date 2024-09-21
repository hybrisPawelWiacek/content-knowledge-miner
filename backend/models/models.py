# /backend/models/models.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import json

@dataclass
class VideoMetadata:
    video_id: str
    title: str
    description: str
    published_at: str
    duration: str
    view_count: int
    like_count: int
    comment_count: int
    transcript_text: str = ''
    key_topics: List[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)  # New field

    def to_airtable_fields(self):
        return {
            'Video ID': self.video_id,
            'Title': self.title,
            'Description': self.description,
            'Published At': datetime.strptime(self.published_at, '%Y-%m-%dT%H:%M:%SZ').strftime('%m/%d/%Y'),
            'Duration': self.duration,
            'View Count': self.view_count,
            'Like Count': self.like_count,
            'Comment Count': self.comment_count,
            'Transcript Text': self.transcript_text,
            'Raw Data': json.dumps(self.raw_data)  # Convert dict to JSON string
            # Add other fields as needed
        }

@dataclass
class UserInput:
    video_id: str
    category: Optional[str] = None
    comments: Optional[str] = None
    highlights: Optional[str] = None
    quality_rating: Optional[int] = None

@dataclass
class Summary:
    video_id: str
    summary_text: str
    key_topics: List[str]
    def to_airtable_fields(self) -> Dict[str, Any]:
        return {
            'Video ID': [self.video_id],  # This should be an array with one record ID
            'Summary Text': self.summary_text,
            'Key Topics': ', '.join(self.key_topics)  # Assuming this is a text field, not a linked record
        }