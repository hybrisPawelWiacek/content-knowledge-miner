# /backend/models/models.py

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

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
