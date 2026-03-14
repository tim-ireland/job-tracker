#!/bin/bash
# Startup script for uvicorn with conditional reload

if [ "$UVICORN_RELOAD" = "1" ]; then
    echo "🔄 Starting in DEVELOPMENT mode (auto-reload enabled)"
    exec uvicorn job_tracker.app:app --host 0.0.0.0 --port 8000 --reload
else
    echo "🚀 Starting in PRODUCTION mode"
    exec uvicorn job_tracker.app:app --host 0.0.0.0 --port 8000
fi
