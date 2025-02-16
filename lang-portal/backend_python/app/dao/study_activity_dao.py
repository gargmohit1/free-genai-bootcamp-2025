import sqlite3
from typing import List, Dict, Optional, Tuple

class StudyActivityDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_study_activities(self, page: int = 1, per_page: int = 10) -> Tuple[List[Dict], int]:
        """Get paginated list of study activities"""
        offset = (page - 1) * per_page
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute('SELECT COUNT(*) FROM study_activities')
            total_count = cursor.fetchone()[0]
            
            # Get paginated activities
            cursor.execute('''
                SELECT id, name, url, created_at 
                FROM study_activities 
                ORDER BY id 
                LIMIT ? OFFSET ?
            ''', (per_page, offset))
            
            activities = [
                {
                    'id': row[0],
                    'name': row[1],
                    'url': row[2],
                    'created_at': row[3]
                }
                for row in cursor.fetchall()
            ]
            
            return activities, total_count
            
        finally:
            conn.close()

    def get_study_activity_by_id(self, activity_id: int) -> Optional[Dict]:
        """Get a study activity by its ID"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, url, created_at 
                FROM study_activities 
                WHERE id = ?
            ''', (activity_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'url': row[2],
                    'created_at': row[3]
                }
            return None
            
        finally:
            conn.close()

    def create_study_activity(self, name: str, url: str) -> Dict:
        """Create a new study activity"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO study_activities (name, url)
                VALUES (?, ?)
            ''', (name, url))
            
            activity_id = cursor.lastrowid
            conn.commit()
            
            return self.get_study_activity_by_id(activity_id)
            
        finally:
            conn.close()

    def update_study_activity(self, activity_id: int, name: str, url: str) -> Optional[Dict]:
        """Update an existing study activity"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE study_activities 
                SET name = ?, url = ?
                WHERE id = ?
            ''', (name, url, activity_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                return self.get_study_activity_by_id(activity_id)
            return None
            
        finally:
            conn.close()

    def delete_study_activity(self, activity_id: int) -> bool:
        """Delete a study activity by its ID"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM study_activities WHERE id = ?', (activity_id,))
            
            success = cursor.rowcount > 0
            if success:
                conn.commit()
            return success
            
        finally:
            conn.close()
