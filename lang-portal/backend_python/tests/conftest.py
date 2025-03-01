import os
import tempfile
import pytest
from app import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test"""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })
    
    # Initialize the test database
    with app.app_context():
        init_db(db_path)
    
    yield app
    
    # Clean up the temporary file
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()

@pytest.fixture
def db_path(app):
    """Get the path to the test database"""
    return app.config['DATABASE']

def init_db(db_path):
    """Initialize the test database with schema"""
    import sqlite3
    
    # Read schema file
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'migrations', '001_initial_schema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    # Create tables
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(schema)
        conn.commit()
    finally:
        conn.close()
