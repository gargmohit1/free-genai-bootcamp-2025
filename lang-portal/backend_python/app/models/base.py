from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class BaseModel:
    """Base model class with common fields and methods"""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convert model to dictionary"""
        result = {}
        for field in self.__dataclass_fields__:
            value = getattr(self, field)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[field] = value
        return result
    
    @classmethod
    def from_dict(cls, data: dict) -> 'BaseModel':
        """Create model instance from dictionary"""
        # Convert string timestamps to datetime objects
        for field in ['created_at', 'updated_at']:
            if field in data and data[field]:
                data[field] = datetime.fromisoformat(data[field].replace('Z', '+00:00'))
        return cls(**data)
