from flask import jsonify

def success_response(data=None, message="Success"):
    """Create a success response"""
    response = {
        "status": "success",
        "message": message
    }
    if data is not None:
        response["data"] = data
    return jsonify(response)

def error_response(message="An error occurred", code="ERROR", status_code=400):
    """Create an error response"""
    response = {
        "status": "error",
        "message": message,
        "error": {
            "code": code,
            "details": message
        }
    }
    return jsonify(response), status_code

def not_found_error(resource="Resource"):
    """Create a not found error response"""
    return error_response(
        message=f"{resource} not found",
        code="NOT_FOUND",
        status_code=404
    )

def validation_error(errors):
    """Create a validation error response"""
    if isinstance(errors, str):
        errors = [errors]
    return error_response(
        message="Validation error",
        code="VALIDATION_ERROR",
        status_code=400
    )
