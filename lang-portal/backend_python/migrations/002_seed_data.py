import sqlite3
import json
from pathlib import Path

def seed_database():
    """Seed the database with initial data from JSON files"""
    # Get the paths
    migrations_dir = Path(__file__).parent
    seed_dir = migrations_dir.parent / 'seed'
    db_path = migrations_dir.parent / 'app.db'
    
    # Connect to SQLite database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Create groups for verbs and adjectives
        cursor.execute('''
            INSERT INTO groups (name, description) VALUES 
            ('Verbs', 'Common Japanese verbs'),
            ('Adjectives', 'Common Japanese adjectives')
        ''')
        verb_group_id = cursor.lastrowid
        cursor.execute('SELECT last_insert_rowid()')
        adj_group_id = verb_group_id + 1
        
        # Load and insert verbs
        with open(seed_dir / 'data_verbs.json', 'r', encoding='utf-8') as f:
            verbs = json.load(f)
            for verb in verbs:
                cursor.execute('''
                    INSERT INTO words (kanji, romaji, meaning) 
                    VALUES (?, ?, ?)
                ''', (verb['kanji'], verb['romaji'], verb['english']))
                word_id = cursor.lastrowid
                
                # Link to verbs group
                cursor.execute('''
                    INSERT INTO group_words (group_id, word_id)
                    VALUES (?, ?)
                ''', (verb_group_id, word_id))
        
        # Load and insert adjectives
        with open(seed_dir / 'data_adjectives.json', 'r', encoding='utf-8') as f:
            adjectives = json.load(f)
            for adj in adjectives:
                cursor.execute('''
                    INSERT INTO words (kanji, romaji, meaning)
                    VALUES (?, ?, ?)
                ''', (adj['kanji'], adj['romaji'], adj['english']))
                word_id = cursor.lastrowid
                
                # Link to adjectives group
                cursor.execute('''
                    INSERT INTO group_words (group_id, word_id)
                    VALUES (?, ?)
                ''', (adj_group_id, word_id))
        
        # Load and insert study activities
        with open(seed_dir / 'study_activities.json', 'r', encoding='utf-8') as f:
            activities = json.load(f)
            for activity in activities:
                cursor.execute('''
                    INSERT INTO study_activities (name, url)
                    VALUES (?, ?)
                ''', (activity['name'], activity['url']))
        
        # Record this seed migration
        cursor.execute('''
            INSERT INTO migrations (migration_file) 
            VALUES ('002_seed_data.py')
        ''')
        
        conn.commit()
        print("Successfully seeded the database!")
        
    except Exception as e:
        print(f"Error during seeding: {str(e)}")
        conn.rollback()
        raise
        
    finally:
        conn.close()

if __name__ == '__main__':
    seed_database()
