### Business Goal: 
A language learning school wants to build a prototype of learning portal which will act as three things:
Inventory of possible vocabulary that can be learned
Act as a  Learning record store (LRS), providing correct and wrong score on practice vocabulary
A unified launchpad to launch different learning apps


### Techincal Requirements 
- Backend app should in python language
- App should use sqllite3 as a database
- App should be use flask api as framework
- Test cases should be part of the app
- Code should follow proper design patter or mvc framework
- API should return json as a response
- API should return status code in response
- API should return error message in response
- API should return success message in response
- API should implement pagination for get request
- API should implement post request
- Add Swagger in code base
- Follow proper naming convention
- Don't use SQL Alchmey, Please use plain database query
- Follow this coding style
    - Route folder should contains only routing information with validation
    - Model folder should contains only model information with getter setter method
    - DAO folder contains all database related query
    - Service class contains business logic
    - Utils folder contains helper function

### Directory Strucutre
lang-portal/
└── backend_python/
    ├── app/
    │   ├── __init__.py          # Flask app initialization
    │   ├── models/              # Combined SQLAlchemy models & Marshmallow schemas
    │   │   ├── __init__.py
    │   │   ├── base.py          # Base model & schema classes
    │   │   ├── word.py          # Word model with its schema
    │   │   ├── group.py         # Group model with its schema
    │   │   ├── study_activity.py
    │   │   └── study_session.py
    │   │
    │   ├── routes/              # API routes/blueprints
    │   │   ├── __init__.py
    │   │   ├── dashboard.py
    │   │   ├── words.py
    │   │   ├── groups.py
    │   │   ├── study_activities.py
    │   │   └── study_sessions.py
    │   │
    │   ├── services/            # Business logic
    │   │   ├── __init__.py
    │   │   ├── word_service.py
    │   │   ├── group_service.py
    │   │   ├── study_service.py
    │   │   └── dashboard_service.py
    │   │
    │   └── utils/               # Helper functions
    │       ├── __init__.py
    │       ├── pagination.py
    │       └── error_handlers.py
    │
    ├── config.py               # Configuration
    ├── migrations/             # Alembic migrations
    ├── tests/                  # Unit and integration tests
    ├── .env                    # Environment variables
    ├── requirements.txt        # Project dependencies
    ├── run.py                  # Application entry point
    └── README.md              # Project documentation
## Technical Specification
### Dashboard API Specification
#### GET /api/dashboard/last_study_session
Return last study session  which will provide information about number of correct words, incorrect words and group information
#### GET /api/dashboard/study_progress
Return information about current study progress, which will show how many words are studied as compared to total number of words availables
#### GET /api/dashboard/quick_stats
Return information about success rate, how many active group, how many sessions and overall study steaks

### Study Activities Specifications
#### GET /api/study_activities
Return list of available study activities.
#### GET /api/study_activities/:id
Return given study activity details.
#### POST /api/study_activities
POST study activities
Request_params:- name, url
#### GET /api/study_activities/:id/study_sessions
Return all session related to study_activities

### Study Sessions Specifications
#### GET /api/study_sessions
RETURN all study_session
#### GET /api/study_sessions/:id
Return study_session by_id
#### POST /api/study_sessions
Request Param :- group_id, study_activity_id
#### POST /api/study_sessions/:id/review
Request Params:- word_id, correct

### Words Specifications
#### GET /api/words
#### GET /api/words/:id
#### POST /api/words
Request Params:- kanji, romaji, english
#### PUT /api/words/:id
Request Params:- kanji, romaji, english

### Word Group Specifications
#### GET /api/groups
#### GET /api/groups/:id
#### POST /api/groups
Request Params:- name
#### PUT /api/groups/:id
Request Params:- name
#### POST /api/groups/:id/words
Request Params:- word_id
Stores data into word_groups table
Update words_count in groups table
#### GET /api/groups/:id/words
Return all words related to group_id

## Database Specifications
words — Stores individual Japanese vocabulary words.
- `id` (Primary Key): Unique identifier for each word
- `kanji` (String, Required): The word written in Japanese kanji
- `romaji` (String, Required): Romanized version of the word
- `english` (String, Required): English translation of the word
- `parts` (JSON, Required): Word components stored in JSON format

groups — Manages collections of words.
- `id` (Primary Key): Unique identifier for each group
- `name` (String, Required): Name of the group
- `words_count` (Integer, Default: 0): Counter cache for the number of words in the group

word_groups — join-table enabling many-to-many relationship between words and groups.
- `word_id` (Foreign Key): References words.id
- `group_id` (Foreign Key): References groups.id

study_activities — Defines different types of study activities available.
- `id` (Primary Key): Unique identifier for each activity
- `name` (String, Required): Name of the activity (e.g., "Flashcards", "Quiz")
- `url` (String, Required): The full URL of the study activity

study_sessions — Records individual study sessions.
- `id` (Primary Key): Unique identifier for each session
- `group_id` (Foreign Key): References groups.id
- `study_activity_id` (Foreign Key): References study_activities.id
- `created_at` (Timestamp, Default: Current Time): When the session was created

word_review_items — Tracks individual word reviews within study sessions.
- `id` (Primary Key): Unique identifier for each review
- `word_id` (Foreign Key): References words.id
- `study_session_id` (Foreign Key): References study_sessions.id
- `correct` (Boolean, Required): Whether the answer was correct
- `created_at` (Timestamp, Default: Current Time): When the review occurred

### Relationships

word belongs to groups through  word_groups
group belongs to words through word_groups
session belongs to a group
session belongs to a study_activity
session has many word_review_items
word_review_item belongs to a study_session
word_review_item belongs to a word

### Migration Scripts
Please add all migration scripts by looking into seed folder and create initial datasets