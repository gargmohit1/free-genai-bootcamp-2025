import pytest
from app.dao.group_dao import GroupDAO
from app.dao.word_dao import WordDAO

@pytest.fixture
def group_dao(db_path):
    return GroupDAO(db_path)

@pytest.fixture
def word_dao(db_path):
    return WordDAO(db_path)

def test_create_group(group_dao):
    # Test creating a group
    group_data = group_dao.create_group(
        name="Test Group",
        description="Test Description"
    )
    
    assert group_data['id'] is not None
    assert group_data['name'] == "Test Group"
    assert group_data['description'] == "Test Description"

def test_get_group_by_id(group_dao):
    # Create a group first
    created = group_dao.create_group(
        name="Test Group",
        description="Test Description"
    )
    
    # Test retrieving the group
    group_data = group_dao.get_group_by_id(created['id'])
    
    assert group_data['id'] == created['id']
    assert group_data['name'] == created['name']
    assert group_data['description'] == created['description']

def test_get_group_by_id_not_found(group_dao):
    # Test retrieving non-existent group
    group_data = group_dao.get_group_by_id(999)
    assert group_data is None

def test_update_group(group_dao):
    # Create a group first
    created = group_dao.create_group(
        name="Test Group",
        description="Test Description"
    )
    
    # Test updating the group
    updated = group_dao.update_group(
        group_id=created['id'],
        name="Updated Group",
        description="Updated Description"
    )
    
    assert updated['id'] == created['id']
    assert updated['name'] == "Updated Group"
    assert updated['description'] == "Updated Description"

def test_update_group_not_found(group_dao):
    # Test updating non-existent group
    updated = group_dao.update_group(
        group_id=999,
        name="Updated Group",
        description="Updated Description"
    )
    assert updated is None

def test_delete_group(group_dao):
    # Create a group first
    created = group_dao.create_group(
        name="Test Group",
        description="Test Description"
    )
    
    # Test deleting the group
    success = group_dao.delete_group(created['id'])
    assert success is True
    
    # Verify group is deleted
    group_data = group_dao.get_group_by_id(created['id'])
    assert group_data is None

def test_delete_group_not_found(group_dao):
    # Test deleting non-existent group
    success = group_dao.delete_group(999)
    assert success is False

def test_get_groups_pagination(group_dao):
    # Create multiple groups
    for i in range(15):
        group_dao.create_group(
            name=f"Group{i}",
            description=f"Description{i}"
        )
    
    # Test first page
    groups, total_count = group_dao.get_groups(page=1, per_page=10)
    assert len(groups) == 10
    assert total_count == 15
    
    # Test second page
    groups, total_count = group_dao.get_groups(page=2, per_page=10)
    assert len(groups) == 5
    assert total_count == 15

def test_get_groups_empty(group_dao):
    # Test getting groups when none exist
    groups, total_count = group_dao.get_groups()
    assert len(groups) == 0
    assert total_count == 0

def test_add_word_to_group(group_dao, word_dao):
    # Create a group and a word
    group = group_dao.create_group(
        name="Test Group",
        description="Test Description"
    )
    word = word_dao.create_word(
        word="test",
        meaning="a trial",
        example="This is a test."
    )
    
    # Test adding word to group
    success = group_dao.add_word_to_group(group['id'], word['id'])
    assert success is True
    
    # Verify word is in group
    words = group_dao.get_group_words(group['id'])
    assert len(words) == 1
    assert words[0]['id'] == word['id']

def test_add_word_to_group_not_found(group_dao):
    # Test adding non-existent word to non-existent group
    success = group_dao.add_word_to_group(999, 999)
    assert success is False

def test_remove_word_from_group(group_dao, word_dao):
    # Create a group and a word
    group = group_dao.create_group(
        name="Test Group",
        description="Test Description"
    )
    word = word_dao.create_word(
        word="test",
        meaning="a trial",
        example="This is a test."
    )
    
    # Add word to group
    group_dao.add_word_to_group(group['id'], word['id'])
    
    # Test removing word from group
    success = group_dao.remove_word_from_group(group['id'], word['id'])
    assert success is True
    
    # Verify word is removed
    words = group_dao.get_group_words(group['id'])
    assert len(words) == 0

def test_remove_word_from_group_not_found(group_dao):
    # Test removing non-existent word from non-existent group
    success = group_dao.remove_word_from_group(999, 999)
    assert success is False
