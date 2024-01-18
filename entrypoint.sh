#!/bin/sh
# entrypoint.sh

# Wait for Postgres to be ready
/wait-for-postgres.sh db

# Run additional setup commands
# e.g., python manage.py migrate

# Start the main application
exec alembic upgrade head 
python -m scripts.SetupDatabase
exec hypercorn main:app --bind 0.0.0.0:53012
