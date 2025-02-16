import sqlite3
from typing import List, Dict, Optional, Tuple

class GroupDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_groups(self, page: int = 1, per_page: int = 10) -> Tuple[List[Dict], int]:
        """Get paginated list of groups"""
        offset = (page - 1) * per_page
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute('SELECT COUNT(*) FROM groups')
            total_count = cursor.fetchone()[0]
            
            # Get paginated groups
            cursor.execute('''
                SELECT id, name, description, created_at 
                FROM groups 
                ORDER BY id 
                LIMIT ? OFFSET ?
            ''', (per_page, offset))
            
            groups = [
                {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3]
                }
                for row in cursor.fetchall()
            ]
            
            return groups, total_count
            
        finally:
            conn.close()

    def get_group_by_id(self, group_id: int) -> Optional[Dict]:
        """Get a group by its ID"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, description, created_at 
                FROM groups 
                WHERE id = ?
            ''', (group_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_at': row[3]
                }
            return None
            
        finally:
            conn.close()

    def get_group_words(self, group_id: int) -> List[Dict]:
        """Get all words in a group"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT w.id, w.word, w.meaning, w.example, w.created_at
                FROM words w
                JOIN group_words gw ON w.id = gw.word_id
                WHERE gw.group_id = ?
            ''', (group_id,))
            
            return [
                {
                    'id': row[0],
                    'word': row[1],
                    'meaning': row[2],
                    'example': row[3],
                    'created_at': row[4]
                }
                for row in cursor.fetchall()
            ]
            
        finally:
            conn.close()

    def create_group(self, name: str, description: Optional[str] = None) -> Dict:
        """Create a new group"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO groups (name, description)
                VALUES (?, ?)
            ''', (name, description))
            
            group_id = cursor.lastrowid
            conn.commit()
            
            return self.get_group_by_id(group_id)
            
        finally:
            conn.close()

    def update_group(self, group_id: int, name: str, description: Optional[str] = None) -> Optional[Dict]:
        """Update an existing group"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE groups 
                SET name = ?, description = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (name, description, group_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                return self.get_group_by_id(group_id)
            return None
            
        finally:
            conn.close()

    def delete_group(self, group_id: int) -> bool:
        """Delete a group by its ID"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM groups WHERE id = ?', (group_id,))
            
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
            cursor.execute('''
                INSERT OR IGNORE INTO group_words (group_id, word_id)
                VALUES (?, ?)
            ''', (group_id, word_id))
            
            success = cursor.rowcount > 0
            if success:
                conn.commit()
            return success
            
        finally:
            conn.close()

    def remove_word_from_group(self, group_id: int, word_id: int) -> bool:
        """Remove a word from a group"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM group_words 
                WHERE group_id = ? AND word_id = ?
            ''', (group_id, word_id))
            
            success = cursor.rowcount > 0
            if success:
                conn.commit()
            return success
            
        finally:
            conn.close()
