#!/bin/bash
# Sync applications from filesystem to database

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Run sync script
python3 sync_applications.py

# Deactivate virtual environment
deactivate
