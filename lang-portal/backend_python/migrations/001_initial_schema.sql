-- Create words table
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kanji TEXT NOT NULL,
    romaji TEXT NOT NULL,
    english TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create groups table
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create group_words table (many-to-many relationship)
CREATE TABLE IF NOT EXISTS group_words (
    group_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (group_id, word_id),
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE
);

-- Create study_activities table
CREATE TABLE IF NOT EXISTS study_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create study_sessions table
CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    study_activity_id INTEGER NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    FOREIGN KEY (study_activity_id) REFERENCES study_activities(id) ON DELETE CASCADE
);

-- Create study_reviews table
CREATE TABLE IF NOT EXISTS study_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_session_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,
    correct BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (study_session_id) REFERENCES study_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE
);

-- Seed data for words
INSERT INTO words (kanji, romaji, english, created_at, updated_at) VALUES
    ('猫', 'neko', 'cat', datetime('now'), datetime('now')),
    ('犬', 'inu', 'dog', datetime('now'), datetime('now')),
    ('鳥', 'tori', 'bird', datetime('now'), datetime('now')),
    ('魚', 'sakana', 'fish', datetime('now'), datetime('now'));

-- Seed data for groups
INSERT INTO groups (name, created_at, updated_at) VALUES
    ('Animals', datetime('now'), datetime('now')),
    ('Fruits', datetime('now'), datetime('now'));

-- Seed data for study activities
INSERT INTO study_activities (name, url, created_at, updated_at) VALUES
    ('Flashcards', 'http://example.com/flashcards', datetime('now'), datetime('now')),
    ('Quizzes', 'http://example.com/quizzes', datetime('now'), datetime('now'));

-- Seed data for study sessions
INSERT INTO study_sessions (group_id, study_activity_id, start_time, created_at) VALUES
    (1, 1, datetime('now'), datetime('now')),
    (2, 2, datetime('now'), datetime('now'));

-- Seed data for study reviews
INSERT INTO study_reviews (study_session_id, word_id, correct, created_at) VALUES
    (1, 1, 1, datetime('now')),
    (1, 2, 0, datetime('now'));