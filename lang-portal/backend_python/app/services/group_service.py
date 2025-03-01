from ..dao.group_dao import GroupDAO
from ..models.group import Group

class GroupService:
    def __init__(self, db_path: str):
        self.group_dao = GroupDAO(db_path)

    def get_groups(self, page: int = 1, per_page: int = 10):
        """Retrieve paginated list of groups"""
        return self.group_dao.get_groups(page, per_page)

    def get_group_by_id(self, group_id: int):
        """Retrieve a group by its ID"""
        return self.group_dao.get_group_by_id(group_id)

    def create_group(self, name: str):
        """Create a new group"""
        return self.group_dao.create_group(name)

    def update_group(self, group_id: int, name: str):
        """Update an existing group"""
        return self.group_dao.update_group(group_id, name)

    def delete_group(self, group_id: int):
        """Delete a group"""
        return self.group_dao.delete_group(group_id)

    def add_word_to_group(self, group_id: int, word_id: int):
        """Add a word to a group"""
        return self.group_dao.add_word_to_group(group_id, word_id)

    def get_words_in_group(self, group_id: int):
        """Get words in a specific group"""
        return self.group_dao.get_words_in_group(group_id)