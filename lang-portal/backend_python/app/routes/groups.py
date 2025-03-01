from flask import Blueprint, request, jsonify
from ..services.group_service import GroupService
from ..models.group import Group
from flask import Blueprint, request, current_app

bp = Blueprint('groups', __name__, url_prefix='/api/groups')

def get_group_service():
    return GroupService(current_app.config['DATABASE'])
    # Your logic for retrieving groups
@bp.route('', methods=['GET'])
def get_groups():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    groups = get_group_service().get_groups(page, per_page)
    return jsonify({"status": "success", "data": groups})

@bp.route('/<int:group_id>', methods=['GET'])
def get_group(group_id):
    group = get_group_service().get_group_by_id(group_id)
    if group:
        return jsonify({"status": "success", "data": group})
    return jsonify({"status": "error", "message": "Group not found"}), 404

@bp.route('', methods=['POST'])
def create_group():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"status": "error", "message": "Name is required"}), 400
    group = get_group_service().create_group(name)
    return jsonify({"status": "success", "data": group}), 201

@bp.route('/<int:group_id>', methods=['PUT'])
def update_group(group_id):
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"status": "error", "message": "Name is required"}), 400
    group = get_group_service().update_group(group_id, name)
    if group:
        return jsonify({"status": "success", "data": group})
    return jsonify({"status": "error", "message": "Group not found"}), 404

@bp.route('/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    success = get_group_service().delete_group(group_id)
    if success:
        return jsonify({"status": "success", "message": "Group deleted"})
    return jsonify({"status": "error", "message": "Group not found"}), 404

@bp.route('/<int:group_id>/words', methods=['POST'])
def add_word():
    data = request.get_json()
    word_id = data.get('word_id')
    if not word_id:
        return jsonify({"status": "error", "message": "Word ID is required"}), 400
    success = get_group_service().add_word_to_group(group_id, word_id)
    if success:
        return jsonify({"status": "success", "message": "Word added to group"}), 201
    return jsonify({"status": "error", "message": "Failed to add word to group"}), 400

@bp.route('/<int:group_id>/words', methods=['GET'])
def get_words(group_id):
    words = get_group_service().get_words_in_group(group_id)
    return jsonify({"status": "success", "data": words})