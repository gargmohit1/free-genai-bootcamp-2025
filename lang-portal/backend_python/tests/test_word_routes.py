import pytest
import json

def test_get_words(client):
    # Test getting empty list of words
    response = client.get('/api/words')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 0
    assert data['meta']['total_count'] == 0

def test_create_word(client):
    # Test creating a word
    response = client.post('/api/words', json={
        'word': 'test',
        'meaning': 'a trial',
        'example': 'This is a test.'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['data']['word'] == 'test'
    assert data['data']['meaning'] == 'a trial'
    assert data['data']['example'] == 'This is a test.'

def test_create_word_invalid(client):
    # Test creating a word with invalid data
    response = client.post('/api/words', json={
        'meaning': 'a trial',
        'example': 'This is a test.'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data

def test_get_word(client):
    # Create a word first
    create_response = client.post('/api/words', json={
        'word': 'test',
        'meaning': 'a trial',
        'example': 'This is a test.'
    })
    word_id = json.loads(create_response.data)['data']['id']
    
    # Test getting the word
    response = client.get(f'/api/words/{word_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['id'] == word_id
    assert data['data']['word'] == 'test'

def test_get_word_not_found(client):
    # Test getting non-existent word
    response = client.get('/api/words/999')
    assert response.status_code == 404

def test_update_word(client):
    # Create a word first
    create_response = client.post('/api/words', json={
        'word': 'test',
        'meaning': 'a trial',
        'example': 'This is a test.'
    })
    word_id = json.loads(create_response.data)['data']['id']
    
    # Test updating the word
    response = client.put(f'/api/words/{word_id}', json={
        'word': 'updated',
        'meaning': 'new meaning',
        'example': 'New example'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['word'] == 'updated'
    assert data['data']['meaning'] == 'new meaning'

def test_update_word_not_found(client):
    # Test updating non-existent word
    response = client.put('/api/words/999', json={
        'word': 'updated',
        'meaning': 'new meaning',
        'example': 'New example'
    })
    assert response.status_code == 404

def test_delete_word(client):
    # Create a word first
    create_response = client.post('/api/words', json={
        'word': 'test',
        'meaning': 'a trial',
        'example': 'This is a test.'
    })
    word_id = json.loads(create_response.data)['data']['id']
    
    # Test deleting the word
    response = client.delete(f'/api/words/{word_id}')
    assert response.status_code == 200
    
    # Verify word is deleted
    get_response = client.get(f'/api/words/{word_id}')
    assert get_response.status_code == 404

def test_delete_word_not_found(client):
    # Test deleting non-existent word
    response = client.delete('/api/words/999')
    assert response.status_code == 404

def test_get_words_pagination(client):
    # Create multiple words
    for i in range(15):
        client.post('/api/words', json={
            'word': f'test{i}',
            'meaning': f'meaning{i}',
            'example': f'example{i}'
        })
    
    # Test first page
    response = client.get('/api/words?page=1&per_page=10')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 10
    assert data['meta']['total_count'] == 15
    assert data['meta']['total_pages'] == 2
    
    # Test second page
    response = client.get('/api/words?page=2&per_page=10')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) == 5
    assert data['meta']['total_count'] == 15
    assert data['meta']['total_pages'] == 2

def test_get_words_invalid_pagination(client):
    # Test invalid page number
    response = client.get('/api/words?page=0')
    assert response.status_code == 400
    
    # Test invalid per_page
    response = client.get('/api/words?per_page=0')
    assert response.status_code == 400
