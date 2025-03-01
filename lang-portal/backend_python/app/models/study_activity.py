from dataclasses import dataclass, field
from .base import BaseModel

@dataclass
class StudyActivity(BaseModel):
    name: str = field(default="Default Study Activity")
    url: str = field(default="http://default.url")

    def __post_init__(self):
        if not self.name:
            raise ValueError("Name is required for StudyActivity.")
        if not self.url:
            raise ValueError("URL is required for StudyActivity.")