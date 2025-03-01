# /Users/mohitgarg/Desktop/Projects/free-genai-bootcamp-2025/lang-portal/backend_python/app/services/study_session_service.py

from ..dao.study_session_dao import StudySessionDAO
from ..models.study_session import StudySession, StudyReview

class StudySessionService:
    def __init__(self, db_path: str):
        self.dao = StudySessionDAO(db_path)

    def add_study_session(self, study_activity_id: int, group_id: int) -> bool:
        """Add a study session associated with a study activity."""
        return self.dao.create_study_session(study_activity_id, group_id)

    def get_study_sessions(self, activity_id: int) -> list:
        """Retrieve all study sessions for a specific study activity."""
        return self.dao.get_study_session_by_id(activity_id,True)

    def record_word_reviews(self, session_id: int, reviews: list) -> bool:
        """Record word reviews for a specific study session."""
        # Logic to process and save reviews
        for review in reviews:
            # Save each review to the database (implement this in the DAO)
            self.dao.add_review(session_id, review['word_id'], review['correct'])
        return True

    def get_study_session_progress(self, session_id: int) -> dict:
        """Retrieve progress of a specific study session."""
        # Logic to calculate and return progress
        return {"progress": "some progress data"}  # Replace with actual logic
    
    def get_all_study_sessions(self) -> list:
        """Retrieve all study sessions."""
        return self.dao.get_all_study_sessions()  # Implement this in DAO as well