from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import os

def create_app(test_config=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # Default configuration
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'lang_portal.db'),
        SECRET_KEY='dev'
    )
    
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.update(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Register blueprints
    from .routes import words,groups,study_activities, study_sessions,dashboard
    app.register_blueprint(words.bp)
    app.register_blueprint(groups.bp)
    app.register_blueprint(study_activities.bp)
    app.register_blueprint(study_sessions.bp)
    app.register_blueprint(dashboard.bp)
    
    # Register Swagger UI blueprint
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swagger_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Language Learning Portal API"
        }
    )
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)
    
    # Route to serve swagger.json
    @app.route('/static/swagger.json')
    def serve_swagger_spec():
        return send_from_directory(app.root_path, 'static/swagger.json')
    
    return app
