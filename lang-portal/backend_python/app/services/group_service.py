from typing import Optional, Tuple, List
from ..models.group import Group
from ..dao.group_dao import GroupDAO

class GroupService:
    def __init__(self, group_dao: GroupDAO):
        self.group_dao = group_dao

    def get_groups(self, page: int = 1, per_page: int = 10) -> Tuple[List[Group], int]:
        """Get paginated list of groups"""
        groups_data, total_count = self.group_dao.get_groups(page, per_page)
        groups = [Group.from_dict(group_data) for group_data in groups_data]
        return groups, total_count

    def get_group(self, group_id: int) -> Optional[Group]:
        """Get a group by its ID"""
        group_data = self.group_dao.get_group_by_id(group_id)
        return Group.from_dict(group_data) if group_data else None

    def get_group_words(self, group_id: int) -> List[dict]:
        """Get all words in a group"""
        return self.group_dao.get_group_words(group_id)

    def create_group(self, group: Group) -> Tuple[Optional[Group], List[str]]:
        """Create a new group"""
        # Validate group data
        errors = group.validate()
        if errors:
            return None, errors

        # Create group in database
        group_data = self.group_dao.create_group(
            name=group.name,
            description=group.description
        )
        return Group.from_dict(group_data), []

    def update_group(self, group_id: int, group: Group) -> Tuple[Optional[Group], List[str]]:
        """Update an existing group"""
        # Validate group data
        errors = group.validate()
        if errors:
            return None, errors

        # Update group in database
        group_data = self.group_dao.update_group(
            group_id=group_id,
            name=group.name,
            description=group.description
        )
        return (Group.from_dict(group_data), []) if group_data else (None, ["Group not found"])

    def delete_group(self, group_id: int) -> bool:
        """Delete a group by its ID"""
        return self.group_dao.delete_group(group_id)

    def add_word_to_group(self, group_id: int, word_id: int) -> bool:
        """Add a word to a group"""
        return self.group_dao.add_word_to_group(group_id, word_id)

    def remove_word_from_group(self, group_id: int, word_id: int) -> bool:
        """Remove a word from a group"""
        return self.group_dao.remove_word_from_group(group_id, word_id)
