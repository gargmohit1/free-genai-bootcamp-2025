from flask import Blueprint, request, jsonify
from ..models.group import Group
from ..services.group_service import GroupService
from ..dao.group_dao import GroupDAO
import os

# Create blueprint
groups_bp = Blueprint('groups', __name__)

# Initialize DAO and service
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app.db')
group_dao = GroupDAO(db_path)
group_service = GroupService(group_dao)

@groups_bp.route('/api/groups', methods=['GET'])
def get_groups():
    """Get paginated list of groups"""
    try:
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Validate pagination parameters
        if page < 1 or per_page < 1:
            return jsonify({
                'error': 'Invalid pagination parameters'
            }), 400
            
        # Get groups
        groups, total_count = group_service.get_groups(page, per_page)
        
        # Calculate pagination metadata
        total_pages = (total_count + per_page - 1) // per_page
        
        return jsonify({
            'data': [group.to_dict() for group in groups],
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

@groups_bp.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """Get a group by its ID"""
    try:
        group = group_service.get_group(group_id)
        if not group:
            return jsonify({
                'error': 'Group not found'
            }), 404
            
        return jsonify({
            'data': group.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@groups_bp.route('/api/groups', methods=['POST'])
def create_group():
    """Create a new group"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
            
        # Create group model
        group = Group(
            id=None,
            name=data.get('name'),
            description=data.get('description')
        )
        
        # Create group
        created_group, errors = group_service.create_group(group)
        if errors:
            return jsonify({
                'errors': errors
            }), 400
            
        return jsonify({
            'data': created_group.to_dict(),
            'message': 'Group created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@groups_bp.route('/api/groups/<int:group_id>', methods=['PUT'])
def update_group(group_id):
    """Update an existing group"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
            
        # Create group model
        group = Group(
            id=group_id,
            name=data.get('name'),
            description=data.get('description')
        )
        
        # Update group
        updated_group, errors = group_service.update_group(group_id, group)
        if errors:
            return jsonify({
                'errors': errors
            }), 400 if 'not found' not in errors[0].lower() else 404
            
        return jsonify({
            'data': updated_group.to_dict(),
            'message': 'Group updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@groups_bp.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """Delete a group by its ID"""
    try:
        success = group_service.delete_group(group_id)
        if not success:
            return jsonify({
                'error': 'Group not found'
            }), 404
            
        return jsonify({
            'message': 'Group deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@groups_bp.route('/api/groups/<int:group_id>/words', methods=['GET'])
def get_group_words(group_id):
    """Get all words in a group"""
    try:
        # First check if group exists
        group = group_service.get_group(group_id)
        if not group:
            return jsonify({
                'error': 'Group not found'
            }), 404
            
        words = group_service.get_group_words(group_id)
        return jsonify({
            'data': words
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@groups_bp.route('/api/groups/<int:group_id>/words/<int:word_id>', methods=['POST'])
def add_word_to_group(group_id, word_id):
    """Add a word to a group"""
    try:
        success = group_service.add_word_to_group(group_id, word_id)
        if not success:
            return jsonify({
                'error': 'Group or word not found'
            }), 404
            
        return jsonify({
            'message': 'Word added to group successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@groups_bp.route('/api/groups/<int:group_id>/words/<int:word_id>', methods=['DELETE'])
def remove_word_from_group(group_id, word_id):
    """Remove a word from a group"""
    try:
        success = group_service.remove_word_from_group(group_id, word_id)
        if not success:
            return jsonify({
                'error': 'Word not found in group'
            }), 404
            
        return jsonify({
            'message': 'Word removed from group successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
