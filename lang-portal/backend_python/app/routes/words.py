from flask import Blueprint, request, jsonify
from ..models.word import Word
from ..services.word_service import WordService
from ..dao.word_dao import WordDAO
import os

# Create blueprint
words_bp = Blueprint('words', __name__)

# Initialize DAO and service
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app.db')
word_dao = WordDAO(db_path)
word_service = WordService(word_dao)

@words_bp.route('/api/words', methods=['GET'])
def get_words():
    """Get paginated list of words"""
    try:
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Validate pagination parameters
        if page < 1 or per_page < 1:
            return jsonify({
                'error': 'Invalid pagination parameters'
            }), 400
            
        # Get words
        words, total_count = word_service.get_words(page, per_page)
        
        # Calculate pagination metadata
        total_pages = (total_count + per_page - 1) // per_page
        
        return jsonify({
            'data': [word.to_dict() for word in words],
            'meta': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': total_pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@words_bp.route('/api/words/<int:word_id>', methods=['GET'])
def get_word(word_id):
    """Get a word by its ID"""
    try:
        word = word_service.get_word(word_id)
        if not word:
            return jsonify({
                'error': 'Word not found'
            }), 404
            
        return jsonify({
            'data': word.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@words_bp.route('/api/words', methods=['POST'])
def create_word():
    """Create a new word"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
            
        # Create word model
        word = Word(
            id=None,
            word=data.get('word'),
            meaning=data.get('meaning'),
            example=data.get('example')
        )
        
        # Create word
        created_word, errors = word_service.create_word(word)
        if errors:
            return jsonify({
                'errors': errors
            }), 400
            
        return jsonify({
            'data': created_word.to_dict(),
            'message': 'Word created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@words_bp.route('/api/words/<int:word_id>', methods=['PUT'])
def update_word(word_id):
    """Update an existing word"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
            
        # Create word model
        word = Word(
            id=word_id,
            word=data.get('word'),
            meaning=data.get('meaning'),
            example=data.get('example')
        )
        
        # Update word
        updated_word, errors = word_service.update_word(word_id, word)
        if errors:
            return jsonify({
                'errors': errors
            }), 400 if 'not found' not in errors[0].lower() else 404
            
        return jsonify({
            'data': updated_word.to_dict(),
            'message': 'Word updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@words_bp.route('/api/words/<int:word_id>', methods=['DELETE'])
def delete_word(word_id):
    """Delete a word by its ID"""
    try:
        success = word_service.delete_word(word_id)
        if not success:
            return jsonify({
                'error': 'Word not found'
            }), 404
            
        return jsonify({
            'message': 'Word deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
