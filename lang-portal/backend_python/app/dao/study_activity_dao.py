import sqlite3
from typing import List, Dict, Any
from ..models.study_activity import StudyActivity
from ..models.study_session import StudySession, StudyReview

class StudyActivityDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_activity(self, activity: StudyActivity) -> bool:
        """Create a new study activity in the database."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO study_activities (name, url) VALUES (?, ?)',
                           (activity.name, activity.url))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def get_activity_by_id(self, activity_id: int) -> StudyActivity:
        """Retrieve a study activity by its ID."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT name, url FROM study_activities WHERE id = ?', (activity_id,))
            row = cursor.fetchone()
            if row:
                return StudyActivity(name=row[0], url=row[1])
            return None
        finally:
            conn.close()

    def update_activity(self, activity_id: int, activity: StudyActivity) -> bool:
        """Update an existing study activity."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE study_activities SET name = ?, url = ? WHERE id = ?',
                           (activity.name, activity.url, activity_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete_activity(self, activity_id: int) -> bool:
        """Delete a study activity by its ID."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM study_activities WHERE id = ?', (activity_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def get_all_activities(self, page: int = 1, per_page: int = 10) -> List[StudyActivity]:
        """Retrieve a paginated list of study activities."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            offset = (page - 1) * per_page
            cursor.execute('SELECT name, url,id FROM study_activities LIMIT ? OFFSET ?', (per_page, offset))
            rows = cursor.fetchall()
            return [StudyActivity(name=row[0], url=row[1], id=row[2]) for row in rows]
        finally:
            conn.close()

    def get_study_activities(self, page: int = 1, per_page: int = 10) -> List[StudyActivity]:
        """Get paginated list of study activities."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            offset = (page - 1) * per_page
            cursor.execute('SELECT name, url, id FROM study_activities LIMIT ? OFFSET ?', (per_page, offset))
            rows = cursor.fetchall()
            return [StudyActivity(name=row[0], url=row[1], id=row[2]) for row in rows]
        finally:
            conn.close()

    def add_study_session(self, study_activity_id: int, group_id: int) -> bool:
        """Add a study session associated with a study activity."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO study_sessions (study_activity_id, group_id) VALUES (?, ?)',
                           (study_activity_id, group_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def get_study_sessions(self, id: int) -> List[StudySession]:
        """Retrieve all study sessions for a specific study activity."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM study_sessions WHERE id = ?', (id,))
            rows = cursor.fetchall()
            return [StudySession(id=row[0], group_id=row[1], study_activity_id=row[2]) for row in rows]
        finally:
            conn.close()
