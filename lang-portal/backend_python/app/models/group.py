from dataclasses import dataclass
from typing import Optional
from .base import BaseModel

@dataclass
class Group(BaseModel):
    """Group model representing a collection of words"""
    name: str = "Default Group Name"  # Default value for name

    def validate(self) -> list[str]:
        """Validate group data"""
        errors = []
        if not self.name:
            errors.append("Name is required")
        return errors