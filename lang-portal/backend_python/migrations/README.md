# Database Migrations

This directory contains database migration scripts for the language learning portal.

## Migration Files

- `001_initial_schema.sql`: Creates the initial database schema including tables for words, groups, study activities, and study sessions.

## How to Run Migrations

To run migrations, simply execute the migrate.py script:

```bash
python migrate.py
```

The migration system will:
1. Create a new SQLite database if it doesn't exist
2. Track applied migrations in a `migrations` table
3. Only apply new migrations that haven't been run before
4. Run migrations in order based on their numerical prefix

## Creating New Migrations

To create a new migration:
1. Create a new SQL file with a numerical prefix (e.g., `002_add_new_table.sql`)
2. Write your SQL statements in the file
3. Run the migration script to apply the changes
