# /Users/mohitgarg/Desktop/Projects/free-genai-bootcamp-2025/lang-portal/backend_python/app/dao/dashboard_dao.py

import sqlite3
from typing import Dict

class DashboardDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path
        
    def get_last_study_session(self) -> Dict:
        """Return the last study session details, including correct and incorrect word counts."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            # Query to get the last study session and count correct and incorrect words
            cursor.execute('''
                SELECT ss.id, ss.group_id, ss.study_activity_id, ss.start_time, ss.end_time,
                       SUM(CASE WHEN sr.correct = 1 THEN 1 ELSE 0 END) AS correct_words,
                       SUM(CASE WHEN sr.correct = 0 THEN 1 ELSE 0 END) AS incorrect_words
                FROM study_sessions ss
                LEFT JOIN study_reviews sr ON ss.id = sr.study_session_id
                GROUP BY ss.id
                ORDER BY ss.start_time DESC
                LIMIT 1
            ''')
            row = cursor.fetchone()
            if row:
                return {
                    "session_id": row[0],
                    "group_id": row[1],
                    "study_activity_id": row[2],
                    "start_time": row[3],
                    "end_time": row[4],
                    "correct_words": row[5],
                    "incorrect_words": row[6]
                }
            return {}
        finally:
            conn.close()
    def get_study_progress(self) -> Dict:
        """Return current study progress."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM words')
            total_words = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM study_reviews WHERE correct = 1')
            studied_words = cursor.fetchone()[0]
            return {
                "studied_words": studied_words,
                "total_words": total_words
            }
        finally:
            conn.close()

    def get_quick_stats(self) -> Dict:
        """Return quick statistics."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(DISTINCT group_id) FROM study_sessions')
            active_groups = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM study_sessions')
            total_sessions = cursor.fetchone()[0]
            return {
                "active_groups": active_groups,
                "total_sessions": total_sessions
            }
        finally:
            conn.close()