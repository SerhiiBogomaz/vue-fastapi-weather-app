#!/bin/bash

echo "Applying migrations..."
/workspace/backend/.venv/bin/alembic upgrade head

echo "Starting FastAPI with debugpy..."

exec /workspace/backend/.venv/bin/python -m debugpy --listen 0.0.0.0:5678 \
    -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
