from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import os
from .routes.words import words_bp
from .routes.groups import groups_bp
from .routes.study_activities import study_activities_bp
from .routes.study_sessions import study_sessions_bp
from .routes.dashboard import dashboard_bp

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Default configuration
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'app.db'),
    )

    if test_config is not None:
        # Load the test config if passed in
        app.config.update(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    CORS(app)  # Enable CORS for all routes
    
    # Serve swagger.json
    @app.route('/static/swagger.json')
    def serve_swagger_spec():
        return send_from_directory(app.static_folder, 'swagger.json')
    
    # Configure Swagger UI
    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI
    API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Language Learning Portal API"
        }
    )
    
    # Register blueprints
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(words_bp)
    app.register_blueprint(groups_bp)
    app.register_blueprint(study_activities_bp)
    app.register_blueprint(study_sessions_bp)
    app.register_blueprint(dashboard_bp)
    
    return app
