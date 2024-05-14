#!/bin/bash

# Wait for the database to be ready
while ! nc -z db 5432; do
  sleep 1
done

# Run alembic upgrade
alembic upgrade head
