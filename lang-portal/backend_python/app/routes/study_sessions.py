from flask import Blueprint, request, jsonify
from ..models.study_session import StudySession
from ..services.study_session_service import StudySessionService
from ..dao.study_session_dao import StudySessionDAO
import os

# Create blueprint
study_sessions_bp = Blueprint('study_sessions', __name__)

# Initialize DAO and service
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app.db')
study_session_dao = StudySessionDAO(db_path)
study_session_service = StudySessionService(study_session_dao)

@study_sessions_bp.route('/api/study_sessions', methods=['GET'])
def get_study_sessions():
    """Get paginated list of study sessions"""
    try:
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Validate pagination parameters
        if page < 1 or per_page < 1:
            return jsonify({
                'error': 'Invalid pagination parameters'
            }), 400
            
        # Get sessions
        sessions, total_count = study_session_service.get_study_sessions(page, per_page)
        
        # Calculate pagination metadata
        total_pages = (total_count + per_page - 1) // per_page
        
        return jsonify({
            'data': [session.to_dict() for session in sessions],
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

@study_sessions_bp.route('/api/study_sessions/<int:session_id>', methods=['GET'])
def get_study_session(session_id):
    """Get a study session by its ID"""
    try:
        session = study_session_service.get_study_session(session_id)
        if not session:
            return jsonify({
                'error': 'Study session not found'
            }), 404
            
        return jsonify({
            'data': session.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@study_sessions_bp.route('/api/study_sessions', methods=['POST'])
def create_study_session():
    """Create a new study session"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
            
        # Create session model
        session = StudySession(
            id=None,
            group_id=data.get('group_id'),
            study_activity_id=data.get('study_activity_id')
        )
        
        # Create session
        created_session, errors = study_session_service.create_study_session(session)
        if errors:
            return jsonify({
                'errors': errors
            }), 400
            
        return jsonify({
            'data': created_session.to_dict(),
            'message': 'Study session created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@study_sessions_bp.route('/api/study_sessions/<int:session_id>/end', methods=['POST'])
def end_study_session(session_id):
    """End a study session"""
    try:
        session, errors = study_session_service.end_study_session(session_id)
        if errors:
            return jsonify({
                'errors': errors
            }), 404
            
        return jsonify({
            'data': session.to_dict(),
            'message': 'Study session ended successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@study_sessions_bp.route('/api/study_sessions/<int:session_id>/review', methods=['POST'])
def add_review(session_id):
    """Add a review to a study session"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
            
        word_id = data.get('word_id')
        correct = data.get('correct')
        
        if word_id is None or correct is None:
            return jsonify({
                'error': 'word_id and correct are required'
            }), 400
            
        # Add review
        review, errors = study_session_service.add_review(session_id, word_id, correct)
        if errors:
            return jsonify({
                'errors': errors
            }), 404
            
        return jsonify({
            'data': review,
            'message': 'Review added successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@study_sessions_bp.route('/api/study_sessions/<int:session_id>/stats', methods=['GET'])
def get_session_stats(session_id):
    """Get statistics for a study session"""
    try:
        stats = study_session_service.get_session_stats(session_id)
        if not stats:
            return jsonify({
                'error': 'Study session not found'
            }), 404
            
        return jsonify({
            'data': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
