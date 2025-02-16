from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class StudyReview:
    id: Optional[int]
    study_session_id: int
    word_id: int
    correct: bool
    reviewed_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'StudyReview':
        """Create a StudyReview instance from a dictionary"""
        return cls(
            id=data.get('id'),
            study_session_id=data['study_session_id'],
            word_id=data['word_id'],
            correct=data['correct'],
            reviewed_at=data.get('reviewed_at')
        )

    def to_dict(self) -> dict:
        """Convert StudyReview instance to dictionary"""
        return {
            'id': self.id,
            'study_session_id': self.study_session_id,
            'word_id': self.word_id,
            'correct': self.correct,
            'reviewed_at': self.reviewed_at
        }

@dataclass
class StudySession:
    id: Optional[int]
    group_id: int
    study_activity_id: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    reviews: List[StudyReview] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'StudySession':
        """Create a StudySession instance from a dictionary"""
        reviews = [StudyReview.from_dict(r) for r in data.get('reviews', [])] if data.get('reviews') else None
        return cls(
            id=data.get('id'),
            group_id=data['group_id'],
            study_activity_id=data['study_activity_id'],
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            reviews=reviews
        )

    def to_dict(self) -> dict:
        """Convert StudySession instance to dictionary"""
        return {
            'id': self.id,
            'group_id': self.group_id,
            'study_activity_id': self.study_activity_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'reviews': [r.to_dict() for r in self.reviews] if self.reviews else None
        }

    def validate(self) -> list[str]:
        """Validate study session data"""
        errors = []
        if not self.group_id:
            errors.append("Group ID is required")
        if not self.study_activity_id:
            errors.append("Study Activity ID is required")
        return errors
