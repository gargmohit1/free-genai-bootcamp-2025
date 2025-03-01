import sqlite3
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from ..models.study_session import StudySession, StudyReview
from ..models.word import Word

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
            
            # Get paginated sessions
            cursor.execute('''
                SELECT id, group_id, study_activity_id, start_time, end_time, created_at
                FROM study_sessions 
                ORDER BY id 
                LIMIT ? OFFSET ?
            ''', (per_page, offset))
            
            sessions = [
                StudySession(
                    id=row[0],
                    group_id=row[1],
                    study_activity_id=row[2],
                    start_time=datetime.fromisoformat(row[3]) if row[3] else None,
                    end_time=datetime.fromisoformat(row[4]) if row[4] else None,
                    created_at=datetime.fromisoformat(row[5]) if row[5] else None
                ).to_dict()
                for row in cursor.fetchall()
            ]
            
            return sessions, total_count
            
        finally:
            conn.close()

    def get_study_session_by_id(self, session_id: int, include_reviews: bool = False) -> Optional[Dict]:
        """Get a study session by its ID"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, group_id, study_activity_id, start_time, end_time, created_at
                FROM study_sessions 
                WHERE id = ?
            ''', (session_id,))
            
            row = cursor.fetchone()
            if row:
                session = StudySession(
                    id=row[0],
                    group_id=row[1],
                    study_activity_id=row[2],
                    start_time=datetime.fromisoformat(row[3]) if row[3] else None,
                    end_time=datetime.fromisoformat(row[4]) if row[4] else None,
                    created_at=datetime.fromisoformat(row[5]) if row[5] else None
                )
                
                if include_reviews:
                    cursor.execute('''
                        SELECT sr.id, sr.word_id, sr.correct, sr.created_at,
                               w.kanji, w.romaji, w.english, w.created_at, w.updated_at
                        FROM study_reviews sr
                        JOIN words w ON sr.word_id = w.id
                        WHERE sr.study_session_id = ?
                    ''', (session_id,))
                    
                    session.reviews = [
                        StudyReview(
                            id=row[0],
                            study_session_id=session_id,
                            word_id=row[1],
                            correct=bool(row[2]),
                            created_at=datetime.fromisoformat(row[3]) if row[3] else None,
                            word=Word(
                                id=row[1],
                                kanji=row[4],
                                romaji=row[5],
                                english=row[6],
                                created_at=datetime.fromisoformat(row[7]) if row[7] else None,
                                updated_at=datetime.fromisoformat(row[8]) if row[8] else None
                            )
                        )
                        for row in cursor.fetchall()
                    ]
                
                return session.to_dict()
            return None
            
        finally:
            conn.close()

    def create_study_session(self, group_id: int, study_activity_id: int) -> Dict:
        """Create a new study session"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat()
            cursor.execute('''
                INSERT INTO study_sessions (group_id, study_activity_id, start_time, created_at)
                VALUES (?, ?, ?, ?)
            ''', (group_id, study_activity_id, now, now))
            
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
            now = datetime.utcnow().isoformat()
            cursor.execute('''
                UPDATE study_sessions 
                SET end_time = ?
                WHERE id = ?
            ''', (now, session_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                return self.get_study_session_by_id(session_id)
            return None
            
        finally:
            conn.close()

    def add_review(self, session_id: int, word_id: int, correct: bool) -> Optional[Dict]:
        """Add a word review to a study session"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat()
            cursor.execute('''
                INSERT INTO study_reviews (study_session_id, word_id, correct, created_at)
                VALUES (?, ?, ?, ?)
            ''', (session_id, word_id, correct, now))
            
            review_id = cursor.lastrowid
            conn.commit()
            
            # Return updated session with reviews
            return self.get_study_session_by_id(session_id, include_reviews=True)
            
        finally:
            conn.close()

    def get_session_stats(self, session_id: int) -> Optional[Dict]:
        """Get statistics for a study session"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_reviews,
                    SUM(CASE WHEN correct = 1 THEN 1 ELSE 0 END) as correct_reviews
                FROM study_reviews
                WHERE study_session_id = ?
            ''', (session_id,))
            
            row = cursor.fetchone()
            if row:
                total_reviews = row[0]
                correct_reviews = row[1] or 0
                return {
                    'total_reviews': total_reviews,
                    'correct_reviews': correct_reviews,
                    'accuracy': (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0
                }
            return None
            
        finally:
            conn.close()

    def get_study_progress(self) -> Dict:
        """Get overall study progress"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # Get total words
            cursor.execute('SELECT COUNT(*) FROM words')
            total_words = cursor.fetchone()[0]
            
            # Get studied words (words that have been reviewed at least once)
            cursor.execute('''
                SELECT COUNT(DISTINCT word_id) 
                FROM study_reviews
            ''')
            studied_words = cursor.fetchone()[0]
            
            return {
                'total_words': total_words,
                'studied_words': studied_words,
                'progress_percentage': (studied_words / total_words * 100) if total_words > 0 else 0
            }
            
        finally:
            conn.close()

    def get_quick_stats(self) -> Dict:
        """Get quick overview statistics"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # Get success rate
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_reviews,
                    SUM(CASE WHEN correct = 1 THEN 1 ELSE 0 END) as correct_reviews
                FROM study_reviews
            ''')
            row = cursor.fetchone()
            total_reviews = row[0]
            correct_reviews = row[1] or 0
            success_rate = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0
            
            # Get active groups count
            cursor.execute('SELECT COUNT(*) FROM groups')
            active_groups = cursor.fetchone()[0]
            
            # Get total sessions
            cursor.execute('SELECT COUNT(*) FROM study_sessions')
            total_sessions = cursor.fetchone()[0]
            
            return {
                'success_rate': success_rate,
                'active_groups': active_groups,
                'total_sessions': total_sessions
            }
            
        finally:
            conn.close()

    def get_all_study_sessions(self) -> List[StudySession]:
        """Retrieve all study sessions."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM study_sessions')
            rows = cursor.fetchall()
            return [StudySession(id=row[0], group_id=row[1], study_activity_id=row[2], start_time=row[3]) for row in rows]
        finally:
            conn.close()