from typing import Optional, Tuple, List, Dict
from ..models.study_session import StudySession, StudyReview
from ..dao.study_session_dao import StudySessionDAO

class StudySessionService:
    def __init__(self, study_session_dao: StudySessionDAO):
        self.study_session_dao = study_session_dao

    def get_study_sessions(self, page: int = 1, per_page: int = 10) -> Tuple[List[StudySession], int]:
        """Get paginated list of study sessions"""
        sessions_data, total_count = self.study_session_dao.get_study_sessions(page, per_page)
        sessions = [StudySession.from_dict(session_data) for session_data in sessions_data]
        return sessions, total_count

    def get_study_session(self, session_id: int) -> Optional[StudySession]:
        """Get a study session by its ID"""
        session_data = self.study_session_dao.get_study_session_by_id(session_id)
        return StudySession.from_dict(session_data) if session_data else None

    def create_study_session(self, session: StudySession) -> Tuple[Optional[StudySession], List[str]]:
        """Create a new study session"""
        # Validate session data
        errors = session.validate()
        if errors:
            return None, errors

        # Create session in database
        session_data = self.study_session_dao.create_study_session(
            group_id=session.group_id,
            study_activity_id=session.study_activity_id
        )
        return StudySession.from_dict(session_data), []

    def end_study_session(self, session_id: int) -> Tuple[Optional[StudySession], List[str]]:
        """End a study session"""
        session_data = self.study_session_dao.end_study_session(session_id)
        if not session_data:
            return None, ["Study session not found or already ended"]
        return StudySession.from_dict(session_data), []

    def add_review(self, session_id: int, word_id: int, correct: bool) -> Tuple[Optional[Dict], List[str]]:
        """Add a review to a study session"""
        review_data = self.study_session_dao.add_review(session_id, word_id, correct)
        if not review_data:
            return None, ["Study session not found or already ended"]
        return review_data, []

    def get_session_stats(self, session_id: int) -> Optional[Dict]:
        """Get statistics for a study session"""
        return self.study_session_dao.get_session_stats(session_id)

    def get_last_study_session(self) -> Optional[StudySession]:
        """Get the last study session"""
        session_data = self.study_session_dao.get_last_study_session()
        return StudySession.from_dict(session_data) if session_data else None

    def get_study_progress(self) -> Dict:
        """Get overall study progress"""
        return self.study_session_dao.get_study_progress()

    def get_quick_stats(self) -> Dict:
        """Get quick statistics about study sessions"""
        return self.study_session_dao.get_quick_stats()
