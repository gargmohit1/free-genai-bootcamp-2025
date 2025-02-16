from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class StudyActivity:
    id: Optional[int]
    name: str
    url: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'StudyActivity':
        """Create a StudyActivity instance from a dictionary"""
        return cls(
            id=data.get('id'),
            name=data['name'],
            url=data['url'],
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self) -> dict:
        """Convert StudyActivity instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def validate(self) -> list[str]:
        """Validate study activity data"""
        errors = []
        if not self.name:
            errors.append("Name is required")
        if not self.url:
            errors.append("URL is required")
        return errors
