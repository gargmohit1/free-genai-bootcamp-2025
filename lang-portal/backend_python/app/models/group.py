from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Group:
    id: Optional[int]
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Group':
        """Create a Group instance from a dictionary"""
        return cls(
            id=data.get('id'),
            name=data['name'],
            description=data.get('description'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self) -> dict:
        """Convert Group instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def validate(self) -> list[str]:
        """Validate group data"""
        errors = []
        if not self.name:
            errors.append("Name is required")
        return errors
