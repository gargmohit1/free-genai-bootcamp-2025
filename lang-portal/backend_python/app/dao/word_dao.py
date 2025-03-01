import sqlite3
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from ..models.word import Word

class WordDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_words(self, page: int = 1, per_page: int = 10) -> Tuple[List[Dict], int]:
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
                SELECT id, kanji, romaji, english, created_at, updated_at
                FROM words 
                ORDER BY id 
                LIMIT ? OFFSET ?
            ''', (per_page, offset))
            
            words = [
                Word(
                    id=row[0],
                    kanji=row[1],
                    romaji=row[2],
                    english=row[3],
                    created_at=datetime.fromisoformat(row[4]) if row[4] else None,
                    updated_at=datetime.fromisoformat(row[5]) if row[5] else None
                ).to_dict()
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
                SELECT id, kanji, romaji, english, created_at, updated_at
                FROM words 
                WHERE id = ?
            ''', (word_id,))
            
            row = cursor.fetchone()
            if row:
                return Word(
                    id=row[0],
                    kanji=row[1],
                    romaji=row[2],
                    english=row[3],
                    created_at=datetime.fromisoformat(row[4]) if row[4] else None,
                    updated_at=datetime.fromisoformat(row[5]) if row[5] else None
                ).to_dict()
            return None
            
        finally:
            conn.close()

    def create_word(self, kanji: str, romaji: str, english: str) -> Dict:
        """Create a new word"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat()
            cursor.execute('''
                INSERT INTO words (kanji, romaji, english, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (kanji, romaji, english, now, now))
            
            word_id = cursor.lastrowid
            conn.commit()
            
            return self.get_word_by_id(word_id)
            
        finally:
            conn.close()

    def update_word(self, word_id: int, kanji: str, romaji: str, english: str) -> Optional[Dict]:
        """Update an existing word"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat()
            cursor.execute('''
                UPDATE words 
                SET kanji = ?, romaji = ?, meaning = ?, updated_at = ?
                WHERE id = ?
            ''', (kanji, romaji, english, now, word_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                return self.get_word_by_id(word_id)
            return None
            
        finally:
            conn.close()

    def delete_word(self, word_id: int) -> bool:
        """Delete a word"""
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
def add_word_to_group(self, group_id: int, word_id: int) -> bool:
    """Add a word to a group"""
    conn = self._get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO group_words (group_id, word_id) VALUES (?, ?)', (group_id, word_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def get_words_in_group(self, group_id: int) -> List[Dict]:
    """Get words in a specific group"""
    conn = self._get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT w.id, w.kanji, w.romaji, w.english
            FROM words w
            JOIN group_words gw ON w.id = gw.word_id
            WHERE gw.group_id = ?
        ''', (group_id,))
        return [dict(id=row[0], kanji=row[1], romaji=row[2], english=row[3]) for row in cursor.fetchall()]
    finally:
        conn.close()