# Language Learning Portal Backend

A Flask-based backend API for a language learning portal that serves as:
1. An inventory of Japanese vocabulary
2. A Learning Record Store (LRS) for tracking study progress
3. A unified launchpad for various learning activities

## Setup

1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
cd migrations
python migrate.py
```

4. Run the application:
```bash
python run.py
```

The API will be available at http://localhost:5000

## API Documentation

### Words API
- `GET /api/words` - Get list of words
- `GET /api/words/:id` - Get word details
- `POST /api/words` - Create new word
- `PUT /api/words/:id` - Update word
- `DELETE /api/words/:id` - Delete word

### Groups API
- `GET /api/groups` - Get list of groups
- `GET /api/groups/:id` - Get group details
- `POST /api/groups` - Create new group
- `PUT /api/groups/:id` - Update group
- `DELETE /api/groups/:id` - Delete group
- `POST /api/groups/:id/words/:word_id` - Add word to group
- `DELETE /api/groups/:id/words/:word_id` - Remove word from group

### Study Activities API
- `GET /api/study_activities` - Get list of activities
- `GET /api/study_activities/:id` - Get activity details
- `POST /api/study_activities` - Create new activity
- `PUT /api/study_activities/:id` - Update activity
- `DELETE /api/study_activities/:id` - Delete activity

### Study Sessions API
- `GET /api/study_sessions` - Get list of sessions
- `GET /api/study_sessions/:id` - Get session details
- `POST /api/study_sessions` - Create new session
- `POST /api/study_sessions/:id/end` - End session
- `POST /api/study_sessions/:id/review` - Add word review

### Dashboard API
- `GET /api/dashboard/last_study_session` - Get last session info
- `GET /api/dashboard/study_progress` - Get study progress
- `GET /api/dashboard/quick_stats` - Get quick statistics

## Testing

Run tests using pytest:
```bash
python -m pytest
```
