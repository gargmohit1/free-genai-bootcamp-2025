from ..dao.study_activity_dao import StudyActivityDAO
from ..models.study_activity import StudyActivity
from ..dao.study_activity_dao import StudyActivityDAO
from ..models.study_activity import StudyActivity

class StudyActivityService:
    def __init__(self, db_path: str):
        self.dao = StudyActivityDAO(db_path)

    def create_activity(self, activity: StudyActivity) -> bool:
        """Create a new study activity."""
        return self.dao.create_activity(activity)

    def get_activity_by_id(self, activity_id: int) -> StudyActivity:
        """Retrieve a study activity by its ID."""
        return self.dao.get_activity_by_id(activity_id)

    def update_activity(self, activity_id: int, activity: StudyActivity) -> bool:
        """Update an existing study activity."""
        return self.dao.update_activity(activity_id, activity)

    def delete_activity(self, activity_id: int) -> bool:
        """Delete a study activity by its ID."""
        return self.dao.delete_activity(activity_id)

    def get_all_activities(self, page: int = 1, per_page: int = 10) -> list:
        """Retrieve a paginated list of study activities."""
        return self.dao.get_all_activities(page, per_page)

    def get_study_sessions(self, activity_id: int) -> list:
        """Retrieve all study sessions for a specific study activity."""
        return self.dao.get_study_sessions(activity_id)

    def get_all_activities(self, page: int = 1, per_page: int = 10) -> list:
        """Retrieve a paginated list of study activities."""
        return self.dao.get_study_activities(page, per_page)
    
    def add_study_session(self, activity_id: int, group_id: int) -> bool:
        """Add a study session associated with a study activity."""
        return self.dao.add_study_session(activity_id, group_id)
    
    def get_study_sessions(self, activity_id: int) -> list:
        """Retrieve all study sessions for a specific study activity."""
        return self.dao.get_study_sessions(activity_id)