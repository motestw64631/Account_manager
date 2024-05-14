#!/bin/bash
while ! nc -z db 5432; do   
  echo "Waiting for PostgreSQL to start..."
  sleep 1
done

# Run alembic upgrade
alembic upgrade head

uvicorn app.main:app --host 0.0.0.0 --port 8087