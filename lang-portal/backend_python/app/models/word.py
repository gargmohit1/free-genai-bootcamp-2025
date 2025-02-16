from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Word:
    id: Optional[int]
    word: str
    meaning: str
    example: Optional[str] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Word':
        """Create a Word instance from a dictionary"""
        return cls(
            id=data.get('id'),
            word=data['word'],
            meaning=data['meaning'],
            example=data.get('example'),
            created_at=data.get('created_at')
        )

    def to_dict(self) -> dict:
        """Convert Word instance to dictionary"""
        return {
            'id': self.id,
            'word': self.word,
            'meaning': self.meaning,
            'example': self.example,
            'created_at': self.created_at
        }

    def validate(self) -> list[str]:
        """Validate word data"""
        errors = []
        if not self.word:
            errors.append("Word is required")
        if not self.meaning:
            errors.append("Meaning is required")
        return errors
