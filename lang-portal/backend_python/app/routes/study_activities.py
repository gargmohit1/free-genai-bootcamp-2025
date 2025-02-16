from flask import Blueprint, request, jsonify
from ..models.study_activity import StudyActivity
from ..services.study_activity_service import StudyActivityService
from ..dao.study_activity_dao import StudyActivityDAO
import os

# Create blueprint
study_activities_bp = Blueprint('study_activities', __name__)

# Initialize DAO and service
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app.db')
study_activity_dao = StudyActivityDAO(db_path)
study_activity_service = StudyActivityService(study_activity_dao)

@study_activities_bp.route('/api/study_activities', methods=['GET'])
def get_study_activities():
    """Get paginated list of study activities"""
    try:
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Validate pagination parameters
        if page < 1 or per_page < 1:
            return jsonify({
                'error': 'Invalid pagination parameters'
            }), 400
            
        # Get activities
        activities, total_count = study_activity_service.get_study_activities(page, per_page)
        
        # Calculate pagination metadata
        total_pages = (total_count + per_page - 1) // per_page
        
        return jsonify({
            'data': [activity.to_dict() for activity in activities],
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

@study_activities_bp.route('/api/study_activities/<int:activity_id>', methods=['GET'])
def get_study_activity(activity_id):
    """Get a study activity by its ID"""
    try:
        activity = study_activity_service.get_study_activity(activity_id)
        if not activity:
            return jsonify({
                'error': 'Study activity not found'
            }), 404
            
        return jsonify({
            'data': activity.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@study_activities_bp.route('/api/study_activities', methods=['POST'])
def create_study_activity():
    """Create a new study activity"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
            
        # Create activity model
        activity = StudyActivity(
            id=None,
            name=data.get('name'),
            url=data.get('url')
        )
        
        # Create activity
        created_activity, errors = study_activity_service.create_study_activity(activity)
        if errors:
            return jsonify({
                'errors': errors
            }), 400
            
        return jsonify({
            'data': created_activity.to_dict(),
            'message': 'Study activity created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@study_activities_bp.route('/api/study_activities/<int:activity_id>', methods=['PUT'])
def update_study_activity(activity_id):
    """Update an existing study activity"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
            
        # Create activity model
        activity = StudyActivity(
            id=activity_id,
            name=data.get('name'),
            url=data.get('url')
        )
        
        # Update activity
        updated_activity, errors = study_activity_service.update_study_activity(activity_id, activity)
        if errors:
            return jsonify({
                'errors': errors
            }), 400 if 'not found' not in errors[0].lower() else 404
            
        return jsonify({
            'data': updated_activity.to_dict(),
            'message': 'Study activity updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@study_activities_bp.route('/api/study_activities/<int:activity_id>', methods=['DELETE'])
def delete_study_activity(activity_id):
    """Delete a study activity by its ID"""
    try:
        success = study_activity_service.delete_study_activity(activity_id)
        if not success:
            return jsonify({
                'error': 'Study activity not found'
            }), 404
            
        return jsonify({
            'message': 'Study activity deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
