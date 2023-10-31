#!/bin/sh

alembic upgrade head

# Start your Python application
python src/main.py