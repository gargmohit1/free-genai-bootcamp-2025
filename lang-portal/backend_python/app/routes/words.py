from flask import Blueprint, request, current_app
from ..services.word_service import WordService
from ..utils.error_handlers import success_response, error_response, not_found_error
from ..utils.pagination import get_pagination_params, paginate_response

bp = Blueprint('words', __name__, url_prefix='/api/words')

def get_word_service():
    return WordService(current_app.config['DATABASE'])

@bp.route('', methods=['GET'])
def get_words():
    """Get paginated list of words"""
    try:
        page, per_page = get_pagination_params()
        word_service = get_word_service()
        words, total_count = word_service.get_words(page, per_page)
        
        return success_response(
            paginate_response(words, total_count, page, per_page)
        )
    except Exception as e:
        return error_response(str(e))

@bp.route('/<int:word_id>', methods=['GET'])
def get_word(word_id):
    """Get a word by its ID"""
    try:
        word_service = get_word_service()
        word = word_service.get_word_by_id(word_id)
        
        if not word:
            return not_found_error('Word')
            
        return success_response(word)
    except Exception as e:
        return error_response(str(e))

@bp.route('', methods=['POST'])
def create_word():
    """Create a new word"""
    try:
        word_data = request.get_json()
        if not word_data:
            return error_response("No data provided")
            
        word_service = get_word_service()
        word = word_service.create_word(word_data)
        
        if not word:
            return error_response("Invalid word data")
            
        return success_response(
            word,
            "Word created successfully"
        )
    except Exception as e:
        return error_response(str(e))

@bp.route('/<int:word_id>', methods=['PUT'])
def update_word(word_id):
    """Update an existing word"""
    try:
        word_data = request.get_json()
        if not word_data:
            return error_response("No data provided")
            
        word_service = get_word_service()
        word = word_service.update_word(word_id, word_data)
        
        if not word:
            return not_found_error('Word')
            
        return success_response(
            word,
            "Word updated successfully"
        )
    except Exception as e:
        return error_response(str(e))

@bp.route('/<int:word_id>', methods=['DELETE'])
def delete_word(word_id):
    """Delete a word"""
    try:
        word_service = get_word_service()
        success = word_service.delete_word(word_id)
        
        if not success:
            return not_found_error('Word')
            
        return success_response(
            message="Word deleted successfully"
        )
    except Exception as e:
        return error_response(str(e))
