import pytest
from app.dao.study_session_dao import StudySessionDAO
from app.dao.group_dao import GroupDAO
from app.dao.study_activity_dao import StudyActivityDAO
from app.dao.word_dao import WordDAO

@pytest.fixture
def study_session_dao(db_path):
    return StudySessionDAO(db_path)

@pytest.fixture
def group_dao(db_path):
    return GroupDAO(db_path)

@pytest.fixture
def study_activity_dao(db_path):
    return StudyActivityDAO(db_path)

@pytest.fixture
def word_dao(db_path):
    return WordDAO(db_path)

@pytest.fixture
def test_data(group_dao, study_activity_dao, word_dao):
    # Create test data and return IDs
    group = group_dao.create_group(
        name="Test Group",
        description="Test Description"
    )
    
    activity = study_activity_dao.create_study_activity(
        name="Test Activity",
        url="http://test.com"
    )
    
    word = word_dao.create_word(
        word="test",
        meaning="a trial",
        example="This is a test."
    )
    
    return {
        'group_id': group['id'],
        'activity_id': activity['id'],
        'word_id': word['id']
    }

def test_create_study_session(study_session_dao, test_data):
    # Test creating a study session
    session_data = study_session_dao.create_study_session(
        group_id=test_data['group_id'],
        study_activity_id=test_data['activity_id']
    )
    
    assert session_data['id'] is not None
    assert session_data['group_id'] == test_data['group_id']
    assert session_data['study_activity_id'] == test_data['activity_id']
    assert session_data['start_time'] is not None
    assert session_data['end_time'] is None
    assert session_data['reviews'] == []

def test_get_study_session_by_id(study_session_dao, test_data):
    # Create a study session first
    created = study_session_dao.create_study_session(
        group_id=test_data['group_id'],
        study_activity_id=test_data['activity_id']
    )
    
    # Test retrieving the session
    session_data = study_session_dao.get_study_session_by_id(created['id'])
    
    assert session_data['id'] == created['id']
    assert session_data['group_id'] == created['group_id']
    assert session_data['study_activity_id'] == created['study_activity_id']
    assert session_data['start_time'] is not None
    assert session_data['end_time'] is None

def test_get_study_session_by_id_not_found(study_session_dao):
    # Test retrieving non-existent session
    session_data = study_session_dao.get_study_session_by_id(999)
    assert session_data is None

def test_end_study_session(study_session_dao, test_data):
    # Create a study session first
    created = study_session_dao.create_study_session(
        group_id=test_data['group_id'],
        study_activity_id=test_data['activity_id']
    )
    
    # Test ending the session
    ended = study_session_dao.end_study_session(created['id'])
    
    assert ended['id'] == created['id']
    assert ended['end_time'] is not None

def test_end_study_session_not_found(study_session_dao):
    # Test ending non-existent session
    ended = study_session_dao.end_study_session(999)
    assert ended is None

def test_add_review(study_session_dao, test_data):
    # Create a study session first
    session = study_session_dao.create_study_session(
        group_id=test_data['group_id'],
        study_activity_id=test_data['activity_id']
    )
    
    # Test adding a review
    review = study_session_dao.add_review(
        session_id=session['id'],
        word_id=test_data['word_id'],
        correct=True
    )
    
    assert review['id'] is not None
    assert review['word_id'] == test_data['word_id']
    assert review['correct'] is True
    assert review['reviewed_at'] is not None

def test_add_review_session_not_found(study_session_dao, test_data):
    # Test adding review to non-existent session
    review = study_session_dao.add_review(
        session_id=999,
        word_id=test_data['word_id'],
        correct=True
    )
    assert review is None

def test_get_session_stats(study_session_dao, test_data):
    # Create a session and add some reviews
    session = study_session_dao.create_study_session(
        group_id=test_data['group_id'],
        study_activity_id=test_data['activity_id']
    )
    
    study_session_dao.add_review(session['id'], test_data['word_id'], True)
    study_session_dao.add_review(session['id'], test_data['word_id'], False)
    study_session_dao.add_review(session['id'], test_data['word_id'], True)
    
    # Test getting session stats
    stats = study_session_dao.get_session_stats(session['id'])
    
    assert stats['total_reviews'] == 3
    assert stats['correct_count'] == 2
    assert stats['incorrect_count'] == 1
    assert stats['accuracy'] == pytest.approx(66.67, 0.01)

def test_get_study_sessions_pagination(study_session_dao, test_data):
    # Create multiple sessions
    for _ in range(15):
        study_session_dao.create_study_session(
            group_id=test_data['group_id'],
            study_activity_id=test_data['activity_id']
        )
    
    # Test first page
    sessions, total_count = study_session_dao.get_study_sessions(page=1, per_page=10)
    assert len(sessions) == 10
    assert total_count == 15
    
    # Test second page
    sessions, total_count = study_session_dao.get_study_sessions(page=2, per_page=10)
    assert len(sessions) == 5
    assert total_count == 15

def test_get_study_sessions_empty(study_session_dao):
    # Test getting sessions when none exist
    sessions, total_count = study_session_dao.get_study_sessions()
    assert len(sessions) == 0
    assert total_count == 0

def test_get_study_progress(study_session_dao, test_data):
    # Create a session and add some reviews
    session = study_session_dao.create_study_session(
        group_id=test_data['group_id'],
        study_activity_id=test_data['activity_id']
    )
    
    study_session_dao.add_review(session['id'], test_data['word_id'], True)
    
    # Test getting study progress
    progress = study_session_dao.get_study_progress()
    
    assert progress['total_words'] == 1
    assert progress['studied_words'] == 1
    assert progress['remaining_words'] == 0
    assert progress['progress_percentage'] == 100.0

def test_get_quick_stats(study_session_dao, test_data):
    # Create a session and add some reviews
    session = study_session_dao.create_study_session(
        group_id=test_data['group_id'],
        study_activity_id=test_data['activity_id']
    )
    
    study_session_dao.add_review(session['id'], test_data['word_id'], True)
    study_session_dao.add_review(session['id'], test_data['word_id'], False)
    
    # Test getting quick stats
    stats = study_session_dao.get_quick_stats()
    
    assert stats['total_sessions'] == 1
    assert stats['active_groups'] == 1
    assert stats['total_reviews'] == 2
    assert stats['success_rate'] == 50.0
