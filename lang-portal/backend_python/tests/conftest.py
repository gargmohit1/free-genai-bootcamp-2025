import os
import pytest
import sqlite3
import tempfile
from app import create_app

@pytest.fixture
def app():
    """Create and configure a test Flask app instance"""
    # Create a temporary file to be used as our database
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # Create tables
    with app.app_context():
        with sqlite3.connect(db_path) as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL,
                    meaning TEXT NOT NULL,
                    example TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS group_words (
                    group_id INTEGER,
                    word_id INTEGER,
                    PRIMARY KEY (group_id, word_id),
                    FOREIGN KEY (group_id) REFERENCES groups (id),
                    FOREIGN KEY (word_id) REFERENCES words (id)
                );

                CREATE TABLE IF NOT EXISTS study_activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS study_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER NOT NULL,
                    study_activity_id INTEGER NOT NULL,
                    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (group_id) REFERENCES groups (id),
                    FOREIGN KEY (study_activity_id) REFERENCES study_activities (id)
                );

                CREATE TABLE IF NOT EXISTS study_reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    study_session_id INTEGER NOT NULL,
                    word_id INTEGER NOT NULL,
                    correct BOOLEAN NOT NULL,
                    reviewed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (study_session_id) REFERENCES study_sessions (id),
                    FOREIGN KEY (word_id) REFERENCES words (id)
                );
            ''')

    yield app

    # Clean up the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner"""
    return app.test_cli_runner()

@pytest.fixture
def db_path(app):
    """Get the test database path"""
    return app.config['DATABASE']
