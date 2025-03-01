from flask import Blueprint, request, jsonify, current_app
from ..services.study_session_service import StudySessionService
from ..models.study_session import StudySession

bp = Blueprint('study_sessions', __name__, url_prefix='/api/study_sessions')

def get_study_session_service():
    return StudySessionService(current_app.config['DATABASE'])

@bp.route('', methods=['POST'])
def create_study_session():
    """Creates a new study session."""
    data = request.get_json()
    group_id = data.get('group_id')
    study_activity_id = data.get('study_activity_id')
    success = get_study_session_service().add_study_session(study_activity_id, group_id)
    
    if success:
        return jsonify({"status": "success", "message": "Study session created successfully", "data": {"session_id": "789", "group_id": group_id, "study_activity_id": study_activity_id, "start_time": "2025-02-15T10:30:00Z"}}), 201
    else:
        return jsonify({"status": "error", "message": "Failed to create study session"}), 400

@bp.route('/<int:id>/review', methods=['POST'])
def record_word_reviews(id):
    """Records word reviews for a session."""
    data = request.get_json()
    reviews = data.get('reviews')
    # Logic to record reviews would go here
    # Assuming you have a service method to handle this
    success = get_study_session_service().record_word_reviews(id, reviews)
    return jsonify({"status": "success", "message": "Word reviews recorded successfully"}), 200 if success else 400

@bp.route('/<int:id>', methods=['GET'])
def get_study_session(id):
    """Retrieve details of a specific study session."""
    session = get_study_session_service().get_study_sessions(id)
    return jsonify({"status": "success", "data": session}), 200 if session else 404

@bp.route('/<int:id>', methods=['DELETE'])
def delete_study_session(id):
    """Delete a study session."""
    success = get_study_session_service().delete_study_session(id)
    return jsonify({"status": "success", "message": "Study session deleted successfully"}), 200 if success else 404

@bp.route('/<int:id>/progress', methods=['GET'])
def get_study_session_progress(id):
    """Retrieve progress of a specific study session."""
    progress = get_study_session_service().get_study_session_progress(id)
    return jsonify({"status": "success", "data": progress}), 200 if progress else 404

@bp.route('', methods=['GET'])
def list_study_sessions():
    """Retrieve a list of all study sessions."""
    sessions = get_study_session_service().get_all_study_sessions()  # Assuming you have a method in the service to get all sessions
    return jsonify({"status": "success", "data": sessions}), 200