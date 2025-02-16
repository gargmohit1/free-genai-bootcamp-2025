import sqlite3
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class StudySessionDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_study_sessions(self, page: int = 1, per_page: int = 10) -> Tuple[List[Dict], int]:
        """Get paginated list of study sessions"""
        offset = (page - 1) * per_page
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute('SELECT COUNT(*) FROM study_sessions')
            total_count = cursor.fetchone()[0]
            
            # Get paginated sessions with reviews
            cursor.execute('''
                SELECT 
                    s.id, s.group_id, s.study_activity_id, s.start_time, s.end_time, s.created_at,
                    r.id as review_id, r.word_id, r.correct, r.reviewed_at, r.created_at as review_created_at
                FROM study_sessions s
                LEFT JOIN study_reviews r ON s.id = r.study_session_id
                ORDER BY s.id DESC
                LIMIT ? OFFSET ?
            ''', (per_page, offset))
            
            sessions = {}
            for row in cursor.fetchall():
                session_id = row[0]
                if session_id not in sessions:
                    sessions[session_id] = {
                        'id': row[0],
                        'group_id': row[1],
                        'study_activity_id': row[2],
                        'start_time': row[3],
                        'end_time': row[4],
                        'created_at': row[5],
                        'reviews': []
                    }
                
                # Add review if it exists
                if row[5]:  # if review_id is not None
                    sessions[session_id]['reviews'].append({
                        'id': row[5],
                        'word_id': row[6],
                        'correct': bool(row[7]),
                        'reviewed_at': row[9],
                        'created_at': row[10]
                    })
            
            return list(sessions.values()), total_count
            
        finally:
            conn.close()

    def get_study_session_by_id(self, session_id: int) -> Optional[Dict]:
        """Get a study session by its ID"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # Get session data
            cursor.execute('''
                SELECT id, group_id, study_activity_id, start_time, end_time, created_at
                FROM study_sessions 
                WHERE id = ?
            ''', (session_id,))
            
            session_row = cursor.fetchone()
            if not session_row:
                return None
                
            session = {
                'id': session_row[0],
                'group_id': session_row[1],
                'study_activity_id': session_row[2],
                'start_time': session_row[3],
                'end_time': session_row[4],
                'created_at': session_row[5],
                'reviews': []
            }
            
            # Get reviews for this session
            cursor.execute('''
                SELECT id, word_id, correct, reviewed_at, created_at
                FROM study_reviews
                WHERE study_session_id = ?
            ''', (session_id,))
            
            session['reviews'] = [
                {
                    'id': row[0],
                    'word_id': row[1],
                    'correct': bool(row[2]),
                    'reviewed_at': row[3],
                    'created_at': row[4]
                }
                for row in cursor.fetchall()
            ]
            
            return session
            
        finally:
            conn.close()

    def create_study_session(self, group_id: int, study_activity_id: int) -> Dict:
        """Create a new study session"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO study_sessions (group_id, study_activity_id, start_time)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (group_id, study_activity_id))
            
            session_id = cursor.lastrowid
            conn.commit()
            
            return self.get_study_session_by_id(session_id)
            
        finally:
            conn.close()

    def end_study_session(self, session_id: int) -> Optional[Dict]:
        """End a study session"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE study_sessions 
                SET end_time = CURRENT_TIMESTAMP
                WHERE id = ? AND end_time IS NULL
            ''', (session_id,))
            
            if cursor.rowcount > 0:
                conn.commit()
                return self.get_study_session_by_id(session_id)
            return None
            
        finally:
            conn.close()

    def add_review(self, session_id: int, word_id: int, correct: bool) -> Optional[Dict]:
        """Add a review to a study session"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # First check if the session exists and is not ended
            cursor.execute('''
                SELECT 1 FROM study_sessions 
                WHERE id = ? AND end_time IS NULL
            ''', (session_id,))
            
            if not cursor.fetchone():
                return None
            
            # Add the review
            cursor.execute('''
                INSERT INTO study_reviews (study_session_id, word_id, correct, reviewed_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (session_id, word_id, correct))
            
            review_id = cursor.lastrowid
            conn.commit()
            
            # Get the created review
            cursor.execute('''
                SELECT id, word_id, correct, reviewed_at
                FROM study_reviews
                WHERE id = ?
            ''', (review_id,))
            
            row = cursor.fetchone()
            return {
                'id': row[0],
                'word_id': row[1],
                'correct': bool(row[2]),
                'reviewed_at': row[3]
            }
            
        finally:
            conn.close()

    def get_session_stats(self, session_id: int) -> Dict:
        """Get statistics for a study session"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_reviews,
                    SUM(CASE WHEN correct = 1 THEN 1 ELSE 0 END) as correct_count
                FROM study_reviews
                WHERE study_session_id = ?
            ''', (session_id,))
            
            row = cursor.fetchone()
            total_reviews = row[0]
            correct_count = row[1] or 0
            
            return {
                'total_reviews': total_reviews,
                'correct_count': correct_count,
                'incorrect_count': total_reviews - correct_count,
                'accuracy': (correct_count / total_reviews * 100) if total_reviews > 0 else 0
            }
            
        finally:
            conn.close()

    def get_last_study_session(self) -> Optional[Dict]:
        """Get the last study session"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id FROM study_sessions 
                ORDER BY start_time DESC 
                LIMIT 1
            ''')
            
            row = cursor.fetchone()
            if row:
                return self.get_study_session_by_id(row[0])
            return None
            
        finally:
            conn.close()

    def get_study_progress(self) -> Dict:
        """Get overall study progress"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # Get total words and studied words
            cursor.execute('''
                SELECT 
                    (SELECT COUNT(*) FROM words) as total_words,
                    (SELECT COUNT(DISTINCT word_id) FROM study_reviews) as studied_words
            ''')
            
            row = cursor.fetchone()
            total_words = row[0]
            studied_words = row[1]
            
            return {
                'total_words': total_words,
                'studied_words': studied_words,
                'remaining_words': total_words - studied_words,
                'progress_percentage': (studied_words / total_words * 100) if total_words > 0 else 0
            }
            
        finally:
            conn.close()

    def get_quick_stats(self) -> Dict:
        """Get quick statistics about study sessions"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # Get various stats
            cursor.execute('''
                SELECT 
                    (SELECT COUNT(*) FROM study_sessions) as total_sessions,
                    (SELECT COUNT(*) FROM groups WHERE id IN (
                        SELECT DISTINCT group_id FROM study_sessions
                    )) as active_groups,
                    (SELECT COUNT(*) FROM study_reviews) as total_reviews,
                    (SELECT COUNT(*) FROM study_reviews WHERE correct = 1) as correct_reviews
            ''')
            
            row = cursor.fetchone()
            total_sessions = row[0]
            active_groups = row[1]
            total_reviews = row[2]
            correct_reviews = row[3]
            
            return {
                'total_sessions': total_sessions,
                'active_groups': active_groups,
                'success_rate': (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0,
                'total_reviews': total_reviews
            }
            
        finally:
            conn.close()
