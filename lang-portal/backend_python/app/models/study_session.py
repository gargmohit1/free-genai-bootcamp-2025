from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from .base import BaseModel
from .word import Word

@dataclass
class StudyReview(BaseModel):
    """StudyReview model representing a word review in a study session"""
    study_session_id: int=0      
    word_id: int=0
    correct: bool=False
    word: Optional[Word] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    def validate(self) -> list[str]:
        """Validate study review data"""
        errors = []
        if not self.study_session_id:
            errors.append("Study session ID is required")
        if not self.word_id:
            errors.append("Word ID is required")
        return errors
    
    def to_dict(self) -> dict:
        """Convert review to dictionary, including word if present"""
        result = super().to_dict()
        if self.word:
            result['word'] = self.word.to_dict()
        return result

@dataclass
class StudySession(BaseModel):
    """StudySession model representing a learning session"""
    group_id: int=0
    study_activity_id: int=0
    start_time: datetime=None
    end_time: Optional[datetime] = None
    reviews: Optional[List[StudyReview]] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    def validate(self) -> list[str]:
        """Validate study session data"""
        errors = []
        if not self.group_id:
            errors.append("Group ID is required")
        if not self.study_activity_id:
            errors.append("Study activity ID is required")
        return errors
    
    def to_dict(self) -> dict:
        """Convert session to dictionary, including reviews if present"""
        result = super().to_dict()
        if self.reviews:
            result['reviews'] = [review.to_dict() for review in self.reviews]
        return result
