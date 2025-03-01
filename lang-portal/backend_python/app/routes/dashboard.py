# /Users/mohitgarg/Desktop/Projects/free-genai-bootcamp-2025/lang-portal/backend_python/app/routes/dashboard.py

from flask import Blueprint, jsonify, current_app
from ..services.dashboard_service import DashboardService

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

def get_dashboard_service():
    return DashboardService(current_app.config['DATABASE'])

@bp.route('/last_study_session', methods=['GET'])
def last_study_session():
    """Return last study session."""
    session = get_dashboard_service().get_last_study_session()
    return jsonify({"status": "success", "data": session}), 200

@bp.route('/study_progress', methods=['GET'])
def study_progress():
    """Return study progress."""
    progress = get_dashboard_service().get_study_progress()
    return jsonify({"status": "success", "data": progress}), 200

@bp.route('/quick_stats', methods=['GET'])
def quick_stats():
    """Return quick statistics."""
    stats = get_dashboard_service().get_quick_stats()
    return jsonify({"status": "success", "data": stats}), 200