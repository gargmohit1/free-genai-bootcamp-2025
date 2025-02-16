import sqlite3
from typing import List, Dict, Optional

class WordDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_words(self, page: int = 1, per_page: int = 10) -> tuple[List[Dict], int]:
        """Get paginated list of words"""
        offset = (page - 1) * per_page
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute('SELECT COUNT(*) FROM words')
            total_count = cursor.fetchone()[0]
            
            # Get paginated words
            cursor.execute('''
                SELECT id, word, meaning, example, created_at 
                FROM words 
                ORDER BY id 
                LIMIT ? OFFSET ?
            ''', (per_page, offset))
            
            words = [
                {
                    'id': row[0],
                    'word': row[1],
                    'meaning': row[2],
                    'example': row[3],
                    'created_at': row[4]
                }
                for row in cursor.fetchall()
            ]
            
            return words, total_count
            
        finally:
            conn.close()

    def get_word_by_id(self, word_id: int) -> Optional[Dict]:
        """Get a word by its ID"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, word, meaning, example, created_at 
                FROM words 
                WHERE id = ?
            ''', (word_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'word': row[1],
                    'meaning': row[2],
                    'example': row[3],
                    'created_at': row[4]
                }
            return None
            
        finally:
            conn.close()

    def create_word(self, word: str, meaning: str, example: Optional[str] = None) -> Dict:
        """Create a new word"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO words (word, meaning, example)
                VALUES (?, ?, ?)
            ''', (word, meaning, example))
            
            word_id = cursor.lastrowid
            conn.commit()
            
            return self.get_word_by_id(word_id)
            
        finally:
            conn.close()

    def update_word(self, word_id: int, word: str, meaning: str, example: Optional[str] = None) -> Optional[Dict]:
        """Update an existing word"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE words 
                SET word = ?, meaning = ?, example = ?
                WHERE id = ?
            ''', (word, meaning, example, word_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                return self.get_word_by_id(word_id)
            return None
            
        finally:
            conn.close()

    def delete_word(self, word_id: int) -> bool:
        """Delete a word by its ID"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM words WHERE id = ?', (word_id,))
            
            success = cursor.rowcount > 0
            if success:
                conn.commit()
            return success
            
        finally:
            conn.close()
