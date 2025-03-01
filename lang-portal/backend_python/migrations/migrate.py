import sqlite3
import os
import sys

def init_db(db_path):
    """Initialize the database with schema"""
    print(f"Initializing database at {db_path}")
    
    # Read schema file
    schema_path = os.path.join(os.path.dirname(__file__), '001_initial_schema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    # Connect to database and execute schema
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(schema)
        conn.commit()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == '__main__':
    # Get database path from command line or use default
    db_path = sys.argv[1] if len(sys.argv) > 1 else '../../lang_portal.db'
    init_db(db_path)
