# Language Portal API Documentation

## Common Response Format
All API responses follow this structure:
```json
{
    "status": "success|error",
    "message": "Human readable message",
    "data": {},  // Response data
    "error": {   // Only present if status is "error"
        "code": "ERROR_CODE",
        "details": "Error details"
    }
}
```

## Dashboard APIs

### 1. GET /api/dashboard/last_study_session
Returns information about the user's most recent study session.

**Response:**
```json
{
    "status": "success",
    "data": {
        "session_id": "123",
        "group_name": "JLPT N5 Basic",
        "study_activity": "Flashcards",
        "correct_words": 15,
        "total_words": 20,
        "accuracy": 75.0,
        "date": "2025-02-15T10:30:00Z"
    }
}
```

### 2. GET /api/dashboard/study_progress
Returns study progress information.

**Response:**
```json
{
    "status": "success",
    "data": {
        "total_words_available": 500,
        "words_studied": 200,
        "progress_percentage": 40.0,
        "study_streak_days": 5
    }
}
```

### 3. GET /api/dashboard/quick_stats
Returns quick overview statistics.

**Response:**
```json
{
    "status": "success",
    "data": {
        "success_rate": 75.5,
        "active_groups": 5,
        "total_sessions": 20,
        "study_streak": 7
    }
}
```

## Study Activities APIs

### 1. GET /api/study_activities
Returns list of available study activities.

**Query Parameters:**
- page (optional): int, default=1
- per_page (optional): int, default=10

**Response:**
```json
{
    "status": "success",
    "data": {
        "items": [
            {
                "id": "123",
                "name": "Flashcards",
                "url": "http://example.com/flashcards",
                "description": "Practice with flashcards"
            }
        ],
        "pagination": {
            "current_page": 1,
            "total_pages": 2,
            "total_items": 15,
            "items_per_page": 10
        }
    }
}
```

### 2. GET /api/study_activities/:id
Returns specific study activity details.

**Response:**
```json
{
    "status": "success",
    "data": {
        "id": "123",
        "name": "Flashcards",
        "url": "http://example.com/flashcards",
        "description": "Practice with flashcards",
        "total_sessions": 50
    }
}
```

### 3. POST /api/study_activities
Creates a new study activity.

**Request:**
```json
{
    "name": "Vocabulary Quiz",
    "url": "http://example.com/quiz"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Study activity created successfully",
    "data": {
        "id": "124",
        "name": "Vocabulary Quiz",
        "url": "http://example.com/quiz"
    }
}
```

### 4. GET /api/study_activities/:id/study_sessions
Returns all sessions for a specific study activity.

**Response:**
```json
{
    "status": "success",
    "data": {
        "items": [
            {
                "id": "123",
                "group_name": "JLPT N5 Basic",
                "date": "2025-02-15T10:30:00Z",
                "review_items_count": 20
            }
        ],
        "pagination": {
            "current_page": 1,
            "total_pages": 2,
            "total_items": 15,
            "items_per_page": 10
        }
    }
}
```

## Study Sessions APIs

### 1. GET /api/study_sessions
Returns all study sessions.

**Query Parameters:**
- page (optional): int, default=1
- per_page (optional): int, default=10

**Response:**
```json
{
    "status": "success",
    "data": {
        "items": [
            {
                "id": "123",
                "group_name": "JLPT N5 Basic",
                "activity_name": "Flashcards",
                "review_items_count": 5,
                "date": "2025-02-15T10:30:00Z"
            }
        ],
        "pagination": {
            "current_page": 1,
            "total_pages": 5,
            "total_items": 45,
            "items_per_page": 10
        }
    }
}
```

### 2. GET /api/study_sessions/:id
Returns details of a specific study session.

**Response:**
```json
{
    "status": "success",
    "data": {
        "id": "123",
        "group_name": "JLPT N5 Basic",
        "activity_name": "Flashcards",
        "review_items_count": 5,
        "date": "2025-02-15T10:30:00Z",
        "reviews": [
            {
                "word_id": "456",
                "correct": true
            }
        ]
    }
}
```

### 3. POST /api/study_sessions
Creates a new study session.

**Request:**
```json
{
    "group_id": "123",
    "study_activity_id": "456"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Study session created successfully",
    "data": {
        "session_id": "789",
        "group_id": "123",
        "study_activity_id": "456",
        "start_time": "2025-02-15T10:30:00Z"
    }
}
```

### 4. POST /api/study_sessions/:id/review
Records word reviews for a session.

**Request:**
```json
{
    "reviews": [
        {
            "word_id": "123",
            "correct": true
        }
    ]
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Reviews recorded successfully",
    "data": {
        "session_id": "789",
        "reviews_recorded": 1,
        "session_accuracy": 100.0
    }
}
```

## Words APIs

### 1. GET /api/words
Returns list of words.

**Query Parameters:**
- page (optional): int, default=1
- per_page (optional): int, default=10
- group_id (optional): string
- search (optional): string

**Response:**
```json
{
    "status": "success",
    "data": {
        "items": [
            {
                "id": "123",
                "kanji": "猫",
                "romaji": "neko",
                "english": "cat"
            }
        ],
        "pagination": {
            "current_page": 1,
            "total_pages": 50,
            "total_items": 500,
            "items_per_page": 10
        }
    }
}
```

### 2. GET /api/words/:id
Returns a specific word.

**Response:**
```json
{
    "status": "success",
    "data": {
        "id": "123",
        "kanji": "猫",
        "romaji": "neko",
        "english": "cat"
    }
}
```

### 3. POST /api/words
Creates a new word.

**Request:**
```json
{
    "kanji": "猫",
    "romaji": "neko",
    "english": "cat"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Word created successfully",
    "data": {
        "id": "123",
        "kanji": "猫",
        "romaji": "neko",
        "english": "cat"
    }
}
```

### 4. PUT /api/words/:id
Updates an existing word.

**Request:**
```json
{
    "kanji": "猫",
    "romaji": "neko",
    "english": "cat"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Word updated successfully",
    "data": {
        "id": "123",
        "kanji": "猫",
        "romaji": "neko",
        "english": "cat"
    }
}
```

## Groups APIs

### 1. GET /api/groups
Returns list of word groups.

**Query Parameters:**
- page (optional): int, default=1
- per_page (optional): int, default=10

**Response:**
```json
{
    "status": "success",
    "data": {
        "items": [
            {
                "id": "123",
                "name": "JLPT N5 Basic",
                "words_count": 100,
                "created_at": "2025-02-15T10:30:00Z"
            }
        ],
        "pagination": {
            "current_page": 1,
            "total_pages": 2,
            "total_items": 15,
            "items_per_page": 10
        }
    }
}
```

### 2. GET /api/groups/:id
Returns details of a specific group.

**Response:**
```json
{
    "status": "success",
    "data": {
        "id": "123",
        "name": "JLPT N5 Basic",
        "words_count": 100,
        "created_at": "2025-02-15T10:30:00Z"
    }
}
```

### 3. POST /api/groups
Creates a new group.

**Request:**
```json
{
    "name": "JLPT N5 Basic"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Group created successfully",
    "data": {
        "id": "123",
        "name": "JLPT N5 Basic",
        "words_count": 0,
        "created_at": "2025-02-15T10:30:00Z"
    }
}
```

### 4. PUT /api/groups/:id
Updates an existing group.

**Request:**
```json
{
    "name": "JLPT N5 Advanced"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Group updated successfully",
    "data": {
        "id": "123",
        "name": "JLPT N5 Advanced",
        "words_count": 100,
        "created_at": "2025-02-15T10:30:00Z"
    }
}
```

### 5. POST /api/groups/:id/words
Adds words to a group.

**Request:**
```json
{
    "word_id": "456"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Word added to group successfully",
    "data": {
        "group_id": "123",
        "words_count": 101
    }
}
```

### 6. GET /api/groups/:id/words
Returns all words in a group.

**Response:**
```json
{
    "status": "success",
    "data": {
        "items": [
            {
                "id": "456",
                "kanji": "猫",
                "romaji": "neko",
                "english": "cat"
            }
        ],
        "pagination": {
            "current_page": 1,
            "total_pages": 2,
            "total_items": 15,
            "items_per_page": 10
        }
    }
}
```

## Error Responses

### 400 Bad Request
```json
{
    "status": "error",
    "message": "Invalid request",
    "error": {
        "code": "VALIDATION_ERROR",
        "details": "Required field 'name' is missing"
    }
}
```

### 404 Not Found
```json
{
    "status": "error",
    "message": "Resource not found",
    "error": {
        "code": "NOT_FOUND",
        "details": "The requested resource does not exist"
    }
}
```

### 500 Internal Server Error
```json
{
    "status": "error",
    "message": "Internal server error",
    "error": {
        "code": "INTERNAL_ERROR",
        "details": "An unexpected error occurred"
    }
}
```
