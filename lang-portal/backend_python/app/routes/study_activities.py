from flask import Blueprint, request, jsonify, current_app
from ..services.study_activity_service import StudyActivityService
from ..models.study_activity import StudyActivity

bp = Blueprint('study_activities', __name__, url_prefix='/api/study_activities')

def get_study_activity_service():
    return StudyActivityService(current_app.config['DATABASE'])

@bp.route('', methods=['GET'])
def get_study_activities():
    """Retrieve the list of study activities."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    activities = get_study_activity_service().get_all_activities(page, per_page)
    return jsonify({"status": "success", "data": activities}), 200

@bp.route('', methods=['POST'])
def create_study_activity():
    """Create a new study activity."""
    data = request.get_json()
    activity = StudyActivity(name=data.get('name'), url=data.get('url'))
    success = get_study_activity_service().create_activity(activity)
    return jsonify({"status": "success", "data": activity}), 201 if success else 400

@bp.route('/<int:activity_id>', methods=['GET'])
def get_study_activity(activity_id):
    """Retrieve a specific study activity by ID."""
    activity = get_study_activity_service().get_activity_by_id(activity_id)
    if activity:
        return jsonify({"status": "success", "data": activity}), 200
    return jsonify({"status": "error", "message": "Study activity not found"}), 404

@bp.route('/<int:activity_id>', methods=['PUT'])
def update_study_activity(activity_id):
    """Update an existing study activity."""
    data = request.get_json()
    activity = StudyActivity(name=data.get('name'), url=data.get('url'))
    success = get_study_activity_service().update_activity(activity_id, activity)
    return jsonify({"status": "success", "data": activity}), 200 if success else 404

@bp.route('/<int:activity_id>', methods=['DELETE'])
def delete_study_activity(activity_id):
    """Delete a study activity by its ID."""
    success = get_study_activity_service().delete_activity(activity_id)
    return jsonify({"status": "success", "message": "Study activity deleted"}), 200 if success else 404
