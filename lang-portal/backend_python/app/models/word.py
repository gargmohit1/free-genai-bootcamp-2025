from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from .base import BaseModel

@dataclass
class Word(BaseModel):
    """Word model representing a Japanese vocabulary word"""
    kanji: str = field(default=None)
    romaji: str = field(default=None)
    english: str = field(default=None)
    
    def validate(self) -> list[str]:
        """Validate word data"""
        errors = []
        if not self.kanji:
            errors.append("Kanji is required")
        if not self.romaji:
            errors.append("Romaji is required")
        if not self.english:
            errors.append("English is required")
        return errors
