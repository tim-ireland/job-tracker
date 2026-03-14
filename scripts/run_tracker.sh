#!/bin/bash
# Job Tracker Startup Script

echo "🚀 Starting Job Application Tracker..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Start the application
echo "✅ Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop"
python -m uvicorn job_tracker.app:app --reload --host 0.0.0.0 --port 8000
