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
    
    return {
        'word_id': word_id,
        'group_id': group_id,
        'activity_id': activity_id
    }

def test_get_study_sessions(client):
    # Test getting empty list of sessions
    response = client.get('/api/study_sessions')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 0
    assert data['meta']['total_count'] == 0

def test_create_study_session(client, test_data):
    # Test creating a study session
    response = client.post('/api/study_sessions', json={
        'group_id': test_data['group_id'],
        'study_activity_id': test_data['activity_id']
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['data']['group_id'] == test_data['group_id']
    assert data['data']['study_activity_id'] == test_data['activity_id']
    assert data['data']['start_time'] is not None
    assert data['data']['end_time'] is None

def test_create_study_session_invalid(client):
    # Test creating a study session with invalid data
    response = client.post('/api/study_sessions', json={
        'group_id': 999,
        'study_activity_id': 999
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data

def test_get_study_session(client, test_data):
    # Create a study session first
    create_response = client.post('/api/study_sessions', json={
        'group_id': test_data['group_id'],
        'study_activity_id': test_data['activity_id']
    })
    session_id = json.loads(create_response.data)['data']['id']
    
    # Test getting the session
    response = client.get(f'/api/study_sessions/{session_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['id'] == session_id
    assert data['data']['group_id'] == test_data['group_id']
    assert data['data']['study_activity_id'] == test_data['activity_id']

def test_get_study_session_not_found(client):
    # Test getting non-existent session
    response = client.get('/api/study_sessions/999')
    assert response.status_code == 404

def test_end_study_session(client, test_data):
    # Create a study session first
    create_response = client.post('/api/study_sessions', json={
        'group_id': test_data['group_id'],
        'study_activity_id': test_data['activity_id']
    })
    session_id = json.loads(create_response.data)['data']['id']
    
    # Test ending the session
    response = client.post(f'/api/study_sessions/{session_id}/end')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['end_time'] is not None

def test_end_study_session_not_found(client):
    # Test ending non-existent session
    response = client.post('/api/study_sessions/999/end')
    assert response.status_code == 404

def test_add_review(client, test_data):
    # Create a study session first
    create_response = client.post('/api/study_sessions', json={
        'group_id': test_data['group_id'],
        'study_activity_id': test_data['activity_id']
    })
    session_id = json.loads(create_response.data)['data']['id']
    
    # Test adding a review
    response = client.post(f'/api/study_sessions/{session_id}/review', json={
        'word_id': test_data['word_id'],
        'correct': True
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['data']['word_id'] == test_data['word_id']
    assert data['data']['correct'] is True

def test_add_review_invalid(client, test_data):
    # Create a study session first
    create_response = client.post('/api/study_sessions', json={
        'group_id': test_data['group_id'],
        'study_activity_id': test_data['activity_id']
    })
    session_id = json.loads(create_response.data)['data']['id']
    
    # Test adding a review with missing data
    response = client.post(f'/api/study_sessions/{session_id}/review', json={
        'word_id': test_data['word_id']
    })
    assert response.status_code == 400

def test_add_review_session_not_found(client, test_data):
    # Test adding review to non-existent session
    response = client.post('/api/study_sessions/999/review', json={
        'word_id': test_data['word_id'],
        'correct': True
    })
    assert response.status_code == 404

def test_get_session_stats(client, test_data):
    # Create a study session first
    create_response = client.post('/api/study_sessions', json={
        'group_id': test_data['group_id'],
        'study_activity_id': test_data['activity_id']
    })
    session_id = json.loads(create_response.data)['data']['id']
    
    # Add some reviews
    client.post(f'/api/study_sessions/{session_id}/review', json={
        'word_id': test_data['word_id'],
        'correct': True
    })
    client.post(f'/api/study_sessions/{session_id}/review', json={
        'word_id': test_data['word_id'],
        'correct': False
    })
    
    # Test getting session stats
    response = client.get(f'/api/study_sessions/{session_id}/stats')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['total_reviews'] == 2
    assert data['data']['correct_count'] == 1
    assert data['data']['incorrect_count'] == 1
    assert data['data']['accuracy'] == 50.0

def test_get_session_stats_not_found(client):
    # Test getting stats for non-existent session
    response = client.get('/api/study_sessions/999/stats')
    assert response.status_code == 404

def test_get_study_sessions_pagination(client, test_data):
    # Create multiple sessions
    for _ in range(15):
        client.post('/api/study_sessions', json={
            'group_id': test_data['group_id'],
            'study_activity_id': test_data['activity_id']
        })
    
    # Test first page
    response = client.get('/api/study_sessions?page=1&per_page=10')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 10
    assert data['meta']['total_count'] == 15
    assert data['meta']['total_pages'] == 2
    
    # Test second page
    response = client.get('/api/study_sessions?page=2&per_page=10')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 5
    assert data['meta']['total_count'] == 15
    assert data['meta']['total_pages'] == 2

def test_get_study_sessions_invalid_pagination(client):
    # Test invalid page number
    response = client.get('/api/study_sessions?page=0')
    assert response.status_code == 400
    
    # Test invalid per_page
    response = client.get('/api/study_sessions?per_page=0')
    assert response.status_code == 400
