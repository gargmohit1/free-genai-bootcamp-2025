from flask import request
from math import ceil

def get_pagination_params():
    """Get pagination parameters from request"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Validate parameters
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        if per_page > 100:
            per_page = 100
            
        return page, per_page
    except ValueError:
        return 1, 10

def paginate_response(items, total_count, page, per_page):
    """Create a paginated response"""
    total_pages = ceil(total_count / per_page) if per_page > 0 else 0
    
    return {
        "items": items,
        "pagination": {
            "current_page": page,
            "total_pages": total_pages,
            "total_items": total_count,
            "items_per_page": per_page
        }
    }
