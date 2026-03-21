#!/bin/bash
# Start a demo instance of the job tracker on port 8001 with fictional seed data.
# Safe to run alongside the real instance — uses a completely separate database.

set -e

DEMO_DIR="/tmp/demo-job-tracker"
PORT=8001
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo "Seeding demo database in $DEMO_DIR ..."
DATA_DIR="$DEMO_DIR" python scripts/seed_demo_data.py

echo ""
echo "Starting demo server on http://localhost:$PORT"
echo "Press Ctrl+C to stop"
echo ""

DATA_DIR="$DEMO_DIR" \
DATABASE_URL="sqlite:///$DEMO_DIR/job_applications.db" \
ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}" \
python -m uvicorn job_tracker.app:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --reload
