# /Users/mohitgarg/Desktop/Projects/free-genai-bootcamp-2025/lang-portal/backend_python/app/services/dashboard_service.py

from ..dao.dashboard_dao import DashboardDAO

class DashboardService:
    def __init__(self, db_path: str):
        self.dao = DashboardDAO(db_path)

    def get_last_study_session(self):
        """Get last study session details."""
        return self.dao.get_last_study_session()

    def get_study_progress(self):
        """Get current study progress."""
        return self.dao.get_study_progress()

    def get_quick_stats(self):
        """Get quick statistics."""
        return self.dao.get_quick_stats()