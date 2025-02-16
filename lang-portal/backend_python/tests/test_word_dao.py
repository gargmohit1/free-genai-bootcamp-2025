import pytest
from app.dao.word_dao import WordDAO

@pytest.fixture
def word_dao(db_path):
    return WordDAO(db_path)

def test_create_word(word_dao):
    # Test creating a word
    word_data = word_dao.create_word(
        word="test",
        meaning="a trial",
        example="This is a test."
    )
    
    assert word_data['id'] is not None
    assert word_data['word'] == "test"
    assert word_data['meaning'] == "a trial"
    assert word_data['example'] == "This is a test."

def test_get_word_by_id(word_dao):
    # Create a word first
    created = word_dao.create_word(
        word="test",
        meaning="a trial",
        example="This is a test."
    )
    
    # Test retrieving the word
    word_data = word_dao.get_word_by_id(created['id'])
    
    assert word_data['id'] == created['id']
    assert word_data['word'] == created['word']
    assert word_data['meaning'] == created['meaning']
    assert word_data['example'] == created['example']

def test_get_word_by_id_not_found(word_dao):
    # Test retrieving non-existent word
    word_data = word_dao.get_word_by_id(999)
    assert word_data is None

def test_update_word(word_dao):
    # Create a word first
    created = word_dao.create_word(
        word="test",
        meaning="a trial",
        example="This is a test."
    )
    
    # Test updating the word
    updated = word_dao.update_word(
        word_id=created['id'],
        word="updated",
        meaning="new meaning",
        example="New example"
    )
    
    assert updated['id'] == created['id']
    assert updated['word'] == "updated"
    assert updated['meaning'] == "new meaning"
    assert updated['example'] == "New example"

def test_update_word_not_found(word_dao):
    # Test updating non-existent word
    updated = word_dao.update_word(
        word_id=999,
        word="updated",
        meaning="new meaning",
        example="New example"
    )
    assert updated is None

def test_delete_word(word_dao):
    # Create a word first
    created = word_dao.create_word(
        word="test",
        meaning="a trial",
        example="This is a test."
    )
    
    # Test deleting the word
    success = word_dao.delete_word(created['id'])
    assert success is True
    
    # Verify word is deleted
    word_data = word_dao.get_word_by_id(created['id'])
    assert word_data is None

def test_delete_word_not_found(word_dao):
    # Test deleting non-existent word
    success = word_dao.delete_word(999)
    assert success is False

def test_get_words_pagination(word_dao):
    # Create multiple words
    for i in range(15):
        word_dao.create_word(
            word=f"test{i}",
            meaning=f"meaning{i}",
            example=f"example{i}"
        )
    
    # Test first page
    words, total_count = word_dao.get_words(page=1, per_page=10)
    assert len(words) == 10
    assert total_count == 15
    
    # Test second page
    words, total_count = word_dao.get_words(page=2, per_page=10)
    assert len(words) == 5
    assert total_count == 15

def test_get_words_empty(word_dao):
    # Test getting words when none exist
    words, total_count = word_dao.get_words()
    assert len(words) == 0
    assert total_count == 0
