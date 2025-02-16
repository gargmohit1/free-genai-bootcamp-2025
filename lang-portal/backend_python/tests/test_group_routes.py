import pytest
import json

@pytest.fixture
def word_id(client):
    # Create a word and return its ID
    response = client.post('/api/words', json={
        'word': 'test',
        'meaning': 'a trial',
        'example': 'This is a test.'
    })
    return json.loads(response.data)['data']['id']

def test_get_groups(client):
    # Test getting empty list of groups
    response = client.get('/api/groups')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 0
    assert data['meta']['total_count'] == 0

def test_create_group(client):
    # Test creating a group
    response = client.post('/api/groups', json={
        'name': 'Test Group',
        'description': 'Test Description'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['data']['name'] == 'Test Group'
    assert data['data']['description'] == 'Test Description'

def test_create_group_invalid(client):
    # Test creating a group with invalid data
    response = client.post('/api/groups', json={
        'description': 'Test Description'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data

def test_get_group(client):
    # Create a group first
    create_response = client.post('/api/groups', json={
        'name': 'Test Group',
        'description': 'Test Description'
    })
    group_id = json.loads(create_response.data)['data']['id']
    
    # Test getting the group
    response = client.get(f'/api/groups/{group_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['id'] == group_id
    assert data['data']['name'] == 'Test Group'

def test_get_group_not_found(client):
    # Test getting non-existent group
    response = client.get('/api/groups/999')
    assert response.status_code == 404

def test_update_group(client):
    # Create a group first
    create_response = client.post('/api/groups', json={
        'name': 'Test Group',
        'description': 'Test Description'
    })
    group_id = json.loads(create_response.data)['data']['id']
    
    # Test updating the group
    response = client.put(f'/api/groups/{group_id}', json={
        'name': 'Updated Group',
        'description': 'Updated Description'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['name'] == 'Updated Group'
    assert data['data']['description'] == 'Updated Description'

def test_update_group_not_found(client):
    # Test updating non-existent group
    response = client.put('/api/groups/999', json={
        'name': 'Updated Group',
        'description': 'Updated Description'
    })
    assert response.status_code == 404

def test_delete_group(client):
    # Create a group first
    create_response = client.post('/api/groups', json={
        'name': 'Test Group',
        'description': 'Test Description'
    })
    group_id = json.loads(create_response.data)['data']['id']
    
    # Test deleting the group
    response = client.delete(f'/api/groups/{group_id}')
    assert response.status_code == 200
    
    # Verify group is deleted
    get_response = client.get(f'/api/groups/{group_id}')
    assert get_response.status_code == 404

def test_delete_group_not_found(client):
    # Test deleting non-existent group
    response = client.delete('/api/groups/999')
    assert response.status_code == 404

def test_get_groups_pagination(client):
    # Create multiple groups
    for i in range(15):
        client.post('/api/groups', json={
            'name': f'Group{i}',
            'description': f'Description{i}'
        })
    
    # Test first page
    response = client.get('/api/groups?page=1&per_page=10')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 10
    assert data['meta']['total_count'] == 15
    assert data['meta']['total_pages'] == 2
    
    # Test second page
    response = client.get('/api/groups?page=2&per_page=10')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 5
    assert data['meta']['total_count'] == 15
    assert data['meta']['total_pages'] == 2

def test_get_groups_invalid_pagination(client):
    # Test invalid page number
    response = client.get('/api/groups?page=0')
    assert response.status_code == 400
    
    # Test invalid per_page
    response = client.get('/api/groups?per_page=0')
    assert response.status_code == 400

def test_add_word_to_group(client, word_id):
    # Create a group first
    create_response = client.post('/api/groups', json={
        'name': 'Test Group',
        'description': 'Test Description'
    })
    group_id = json.loads(create_response.data)['data']['id']
    
    # Test adding word to group
    response = client.post(f'/api/groups/{group_id}/words/{word_id}')
    assert response.status_code == 200
    
    # Verify word is in group
    response = client.get(f'/api/groups/{group_id}/words')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 1
    assert data['data'][0]['id'] == word_id

def test_add_word_to_group_not_found(client, word_id):
    # Test adding word to non-existent group
    response = client.post(f'/api/groups/999/words/{word_id}')
    assert response.status_code == 404
    
    # Test adding non-existent word to group
    create_response = client.post('/api/groups', json={
        'name': 'Test Group',
        'description': 'Test Description'
    })
    group_id = json.loads(create_response.data)['data']['id']
    response = client.post(f'/api/groups/{group_id}/words/999')
    assert response.status_code == 404

def test_remove_word_from_group(client, word_id):
    # Create a group first
    create_response = client.post('/api/groups', json={
        'name': 'Test Group',
        'description': 'Test Description'
    })
    group_id = json.loads(create_response.data)['data']['id']
    
    # Add word to group
    client.post(f'/api/groups/{group_id}/words/{word_id}')
    
    # Test removing word from group
    response = client.delete(f'/api/groups/{group_id}/words/{word_id}')
    assert response.status_code == 200
    
    # Verify word is removed
    response = client.get(f'/api/groups/{group_id}/words')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 0

def test_remove_word_from_group_not_found(client, word_id):
    # Test removing word from non-existent group
    response = client.delete(f'/api/groups/999/words/{word_id}')
    assert response.status_code == 404
    
    # Test removing non-existent word from group
    create_response = client.post('/api/groups', json={
        'name': 'Test Group',
        'description': 'Test Description'
    })
    group_id = json.loads(create_response.data)['data']['id']
    response = client.delete(f'/api/groups/{group_id}/words/999')
    assert response.status_code == 404
