import pytest
from app.dao.study_activity_dao import StudyActivityDAO

@pytest.fixture
def study_activity_dao(db_path):
    return StudyActivityDAO(db_path)

def test_create_study_activity(study_activity_dao):
    # Test creating a study activity
    activity_data = study_activity_dao.create_study_activity(
        name="Test Activity",
        url="http://test.com"
    )
    
    assert activity_data['id'] is not None
    assert activity_data['name'] == "Test Activity"
    assert activity_data['url'] == "http://test.com"

def test_get_study_activity_by_id(study_activity_dao):
    # Create a study activity first
    created = study_activity_dao.create_study_activity(
        name="Test Activity",
        url="http://test.com"
    )
    
    # Test retrieving the activity
    activity_data = study_activity_dao.get_study_activity_by_id(created['id'])
    
    assert activity_data['id'] == created['id']
    assert activity_data['name'] == created['name']
    assert activity_data['url'] == created['url']

def test_get_study_activity_by_id_not_found(study_activity_dao):
    # Test retrieving non-existent activity
    activity_data = study_activity_dao.get_study_activity_by_id(999)
    assert activity_data is None

def test_update_study_activity(study_activity_dao):
    # Create a study activity first
    created = study_activity_dao.create_study_activity(
        name="Test Activity",
        url="http://test.com"
    )
    
    # Test updating the activity
    updated = study_activity_dao.update_study_activity(
        activity_id=created['id'],
        name="Updated Activity",
        url="http://updated.com"
    )
    
    assert updated['id'] == created['id']
    assert updated['name'] == "Updated Activity"
    assert updated['url'] == "http://updated.com"

def test_update_study_activity_not_found(study_activity_dao):
    # Test updating non-existent activity
    updated = study_activity_dao.update_study_activity(
        activity_id=999,
        name="Updated Activity",
        url="http://updated.com"
    )
    assert updated is None

def test_delete_study_activity(study_activity_dao):
    # Create a study activity first
    created = study_activity_dao.create_study_activity(
        name="Test Activity",
        url="http://test.com"
    )
    
    # Test deleting the activity
    success = study_activity_dao.delete_study_activity(created['id'])
    assert success is True
    
    # Verify activity is deleted
    activity_data = study_activity_dao.get_study_activity_by_id(created['id'])
    assert activity_data is None

def test_delete_study_activity_not_found(study_activity_dao):
    # Test deleting non-existent activity
    success = study_activity_dao.delete_study_activity(999)
    assert success is False

def test_get_study_activities_pagination(study_activity_dao):
    # Create multiple activities
    for i in range(15):
        study_activity_dao.create_study_activity(
            name=f"Activity{i}",
            url=f"http://test{i}.com"
        )
    
    # Test first page
    activities, total_count = study_activity_dao.get_study_activities(page=1, per_page=10)
    assert len(activities) == 10
    assert total_count == 15
    
    # Test second page
    activities, total_count = study_activity_dao.get_study_activities(page=2, per_page=10)
    assert len(activities) == 5
    assert total_count == 15

def test_get_study_activities_empty(study_activity_dao):
    # Test getting activities when none exist
    activities, total_count = study_activity_dao.get_study_activities()
    assert len(activities) == 0
    assert total_count == 0
