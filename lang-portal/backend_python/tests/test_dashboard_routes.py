import pytest
import json

@pytest.fixture
def test_data(client):
    # Create necessary test data and return their IDs
    
    # Create a word
    word_response = client.post('/api/words', json={
        'word': 'test',
        'meaning': 'a trial',
        'example': 'This is a test.'
    })
    word_id = json.loads(word_response.data)['data']['id']
    
    # Create a group
    group_response = client.post('/api/groups', json={
        'name': 'Test Group',
        'description': 'Test Description'
    })
    group_id = json.loads(group_response.data)['data']['id']
    
    # Add word to group
    client.post(f'/api/groups/{group_id}/words/{word_id}')
    
    # Create a study activity
    activity_response = client.post('/api/study_activities', json={
        'name': 'Test Activity',
        'url': 'http://test.com'
    })
    activity_id = json.loads(activity_response.data)['data']['id']
    
    # Create a study session
    session_response = client.post('/api/study_sessions', json={
        'group_id': group_id,
        'study_activity_id': activity_id
    })
    session_id = json.loads(session_response.data)['data']['id']
    
    # Add some reviews
    client.post(f'/api/study_sessions/{session_id}/review', json={
        'word_id': word_id,
        'correct': True
    })
    client.post(f'/api/study_sessions/{session_id}/review', json={
        'word_id': word_id,
        'correct': False
    })
    
    return {
        'word_id': word_id,
        'group_id': group_id,
        'activity_id': activity_id,
        'session_id': session_id
    }

def test_get_last_session_empty(client):
    # Test getting last session when none exists
    response = client.get('/api/dashboard/last_session')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data'] is None

def test_get_last_session(client, test_data):
    # Test getting last session
    response = client.get('/api/dashboard/last_session')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data'] is not None
    assert data['data']['id'] == test_data['session_id']
    assert data['data']['group_id'] == test_data['group_id']
    assert data['data']['study_activity_id'] == test_data['activity_id']

def test_get_study_progress_empty(client):
    # Test getting study progress when no words exist
    response = client.get('/api/dashboard/progress')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['total_words'] == 0
    assert data['data']['studied_words'] == 0
    assert data['data']['remaining_words'] == 0
    assert data['data']['progress_percentage'] == 0

def test_get_study_progress(client, test_data):
    # Test getting study progress
    response = client.get('/api/dashboard/progress')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['total_words'] == 1
    assert data['data']['studied_words'] == 1
    assert data['data']['remaining_words'] == 0
    assert data['data']['progress_percentage'] == 100.0

def test_get_quick_stats_empty(client):
    # Test getting quick stats when no sessions exist
    response = client.get('/api/dashboard/quick_stats')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['total_sessions'] == 0
    assert data['data']['active_groups'] == 0
    assert data['data']['total_reviews'] == 0
    assert data['data']['success_rate'] == 0

def test_get_quick_stats(client, test_data):
    # Test getting quick stats
    response = client.get('/api/dashboard/quick_stats')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['total_sessions'] == 1
    assert data['data']['active_groups'] == 1
    assert data['data']['total_reviews'] == 2
    assert data['data']['success_rate'] == 50.0
