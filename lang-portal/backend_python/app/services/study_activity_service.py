from typing import Optional, Tuple, List
from ..models.study_activity import StudyActivity
from ..dao.study_activity_dao import StudyActivityDAO

class StudyActivityService:
    def __init__(self, study_activity_dao: StudyActivityDAO):
        self.study_activity_dao = study_activity_dao

    def get_study_activities(self, page: int = 1, per_page: int = 10) -> Tuple[List[StudyActivity], int]:
        """Get paginated list of study activities"""
        activities_data, total_count = self.study_activity_dao.get_study_activities(page, per_page)
        activities = [StudyActivity.from_dict(activity_data) for activity_data in activities_data]
        return activities, total_count

    def get_study_activity(self, activity_id: int) -> Optional[StudyActivity]:
        """Get a study activity by its ID"""
        activity_data = self.study_activity_dao.get_study_activity_by_id(activity_id)
        return StudyActivity.from_dict(activity_data) if activity_data else None

    def create_study_activity(self, activity: StudyActivity) -> Tuple[Optional[StudyActivity], List[str]]:
        """Create a new study activity"""
        # Validate activity data
        errors = activity.validate()
        if errors:
            return None, errors

        # Create activity in database
        activity_data = self.study_activity_dao.create_study_activity(
            name=activity.name,
            url=activity.url
        )
        return StudyActivity.from_dict(activity_data), []

    def update_study_activity(self, activity_id: int, activity: StudyActivity) -> Tuple[Optional[StudyActivity], List[str]]:
        """Update an existing study activity"""
        # Validate activity data
        errors = activity.validate()
        if errors:
            return None, errors

        # Update activity in database
        activity_data = self.study_activity_dao.update_study_activity(
            activity_id=activity_id,
            name=activity.name,
            url=activity.url
        )
        return (StudyActivity.from_dict(activity_data), []) if activity_data else (None, ["Study activity not found"])

    def delete_study_activity(self, activity_id: int) -> bool:
        """Delete a study activity by its ID"""
        return self.study_activity_dao.delete_study_activity(activity_id)
