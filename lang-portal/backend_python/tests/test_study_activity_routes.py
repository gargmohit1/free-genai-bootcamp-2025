import pytest
import json

def test_get_study_activities(client):
    # Test getting empty list of activities
    response = client.get('/api/study_activities')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 0
    assert data['meta']['total_count'] == 0

def test_create_study_activity(client):
    # Test creating a study activity
    response = client.post('/api/study_activities', json={
        'name': 'Test Activity',
        'url': 'http://test.com'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['data']['name'] == 'Test Activity'
    assert data['data']['url'] == 'http://test.com'

def test_create_study_activity_invalid(client):
    # Test creating a study activity with invalid data
    response = client.post('/api/study_activities', json={
        'name': 'Test Activity'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data

def test_get_study_activity(client):
    # Create a study activity first
    create_response = client.post('/api/study_activities', json={
        'name': 'Test Activity',
        'url': 'http://test.com'
    })
    activity_id = json.loads(create_response.data)['data']['id']
    
    # Test getting the activity
    response = client.get(f'/api/study_activities/{activity_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['id'] == activity_id
    assert data['data']['name'] == 'Test Activity'
    assert data['data']['url'] == 'http://test.com'

def test_get_study_activity_not_found(client):
    # Test getting non-existent activity
    response = client.get('/api/study_activities/999')
    assert response.status_code == 404

def test_update_study_activity(client):
    # Create a study activity first
    create_response = client.post('/api/study_activities', json={
        'name': 'Test Activity',
        'url': 'http://test.com'
    })
    activity_id = json.loads(create_response.data)['data']['id']
    
    # Test updating the activity
    response = client.put(f'/api/study_activities/{activity_id}', json={
        'name': 'Updated Activity',
        'url': 'http://updated.com'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['name'] == 'Updated Activity'
    assert data['data']['url'] == 'http://updated.com'

def test_update_study_activity_not_found(client):
    # Test updating non-existent activity
    response = client.put('/api/study_activities/999', json={
        'name': 'Updated Activity',
        'url': 'http://updated.com'
    })
    assert response.status_code == 404

def test_delete_study_activity(client):
    # Create a study activity first
    create_response = client.post('/api/study_activities', json={
        'name': 'Test Activity',
        'url': 'http://test.com'
    })
    activity_id = json.loads(create_response.data)['data']['id']
    
    # Test deleting the activity
    response = client.delete(f'/api/study_activities/{activity_id}')
    assert response.status_code == 200
    
    # Verify activity is deleted
    get_response = client.get(f'/api/study_activities/{activity_id}')
    assert get_response.status_code == 404

def test_delete_study_activity_not_found(client):
    # Test deleting non-existent activity
    response = client.delete('/api/study_activities/999')
    assert response.status_code == 404

def test_get_study_activities_pagination(client):
    # Create multiple activities
    for i in range(15):
        client.post('/api/study_activities', json={
            'name': f'Activity{i}',
            'url': f'http://test{i}.com'
        })
    
    # Test first page
    response = client.get('/api/study_activities?page=1&per_page=10')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 10
    assert data['meta']['total_count'] == 15
    assert data['meta']['total_pages'] == 2
    
    # Test second page
    response = client.get('/api/study_activities?page=2&per_page=10')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 5
    assert data['meta']['total_count'] == 15
    assert data['meta']['total_pages'] == 2

def test_get_study_activities_invalid_pagination(client):
    # Test invalid page number
    response = client.get('/api/study_activities?page=0')
    assert response.status_code == 400
    
    # Test invalid per_page
    response = client.get('/api/study_activities?per_page=0')
    assert response.status_code == 400
