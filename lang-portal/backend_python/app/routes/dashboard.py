from flask import Blueprint, jsonify
from ..services.study_session_service import StudySessionService
from ..dao.study_session_dao import StudySessionDAO
import os

# Create blueprint
dashboard_bp = Blueprint('dashboard', __name__)

# Initialize DAO and service
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app.db')
study_session_dao = StudySessionDAO(db_path)
study_session_service = StudySessionService(study_session_dao)

@dashboard_bp.route('/api/dashboard/last_session', methods=['GET'])
def get_last_session():
    """Get the last study session"""
    try:
        session = study_session_service.get_last_study_session()
        if not session:
            return jsonify({
                'data': None
            }), 200
            
        return jsonify({
            'data': session.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@dashboard_bp.route('/api/dashboard/progress', methods=['GET'])
def get_study_progress():
    """Get overall study progress"""
    try:
        progress = study_session_service.get_study_progress()
        return jsonify({
            'data': progress
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@dashboard_bp.route('/api/dashboard/quick_stats', methods=['GET'])
def get_quick_stats():
    """Get quick statistics about study sessions"""
    try:
        stats = study_session_service.get_quick_stats()
        return jsonify({
            'data': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
