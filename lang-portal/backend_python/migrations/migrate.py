import sqlite3
import os
import sys
from pathlib import Path

def init_db():
    """Initialize the database and run migrations"""
    # Get the directory containing this script
    migrations_dir = Path(__file__).parent
    db_path = migrations_dir.parent / 'app.db'
    
    # Connect to SQLite database (will create if not exists)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Create migrations table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_file TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Get list of migration files
        migration_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.sql')])
        
        # Get already applied migrations
        cursor.execute('SELECT migration_file FROM migrations')
        applied_migrations = {row[0] for row in cursor.fetchall()}
        
        # Apply new migrations
        for migration_file in migration_files:
            if migration_file not in applied_migrations:
                print(f"Applying migration: {migration_file}")
                
                # Read and execute migration file
                with open(migrations_dir / migration_file) as f:
                    migration_sql = f.read()
                    cursor.executescript(migration_sql)
                
                # Record the migration
                cursor.execute('INSERT INTO migrations (migration_file) VALUES (?)', (migration_file,))
                conn.commit()
                print(f"Successfully applied migration: {migration_file}")
        
        print("All migrations completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        conn.rollback()
        sys.exit(1)
        
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
