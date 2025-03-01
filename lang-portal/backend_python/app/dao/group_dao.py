import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
from ..models.group import Group

class GroupDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_groups(self, page: int = 1, per_page: int = 10) -> List[Dict]:
        """Get paginated list of groups"""
        offset = (page - 1) * per_page
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM groups')
            total_count = cursor.fetchone()[0]
            cursor.execute('''
                SELECT id, name, created_at, updated_at
                FROM groups
                ORDER BY id
                LIMIT ? OFFSET ?
            ''', (per_page, offset))
            groups = [
                Group(
                    id=row[0],
                    name=row[1],
                    created_at=datetime.fromisoformat(row[2]) if row[2] else None,
                    updated_at=datetime.fromisoformat(row[3]) if row[3] else None
                ).to_dict()
                for row in cursor.fetchall()
            ]
            return groups
        finally:
            conn.close()

    def get_group_by_id(self, group_id: int) -> Optional[Dict]:
        """Get a group by its ID"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, created_at, updated_at FROM groups WHERE id = ?', (group_id,))
            row = cursor.fetchone()
            if row:
                return Group(
                    id=row[0],
                    name=row[1],
                    created_at=datetime.fromisoformat(row[2]) if row[2] else None,
                    updated_at=datetime.fromisoformat(row[3]) if row[3] else None
                ).to_dict()
            return None
        finally:
            conn.close()

    def create_group(self, name: str) -> Dict:
        """Create a new group"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat()
            cursor.execute('INSERT INTO groups (name, created_at, updated_at) VALUES (?, ?, ?)', (name, now, now))
            group_id = cursor.lastrowid
            conn.commit()
            return self.get_group_by_id(group_id)
        finally:
            conn.close()

    def update_group(self, group_id: int, name: str) -> Optional[Dict]:
        """Update an existing group"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat()
            cursor.execute('UPDATE groups SET name = ?, updated_at = ? WHERE id = ?', (name, now, group_id))
            if cursor.rowcount > 0:
                conn.commit()
                return self.get_group_by_id(group_id)
            return None
        finally:
            conn.close()

    def delete_group(self, group_id: int) -> bool:
        """Delete a group"""
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
