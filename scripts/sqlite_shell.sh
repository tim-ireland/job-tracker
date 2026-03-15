#!/bin/bash
# Script to access SQLite database inside the container

# Container name from docker-compose.yml
CONTAINER_NAME="job-search-tracker"

# Database path inside the container
DB_PATH="/data/job_applications.db"

# Check if container is running
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Error: Container '${CONTAINER_NAME}' is not running."
    echo "Start the container with: docker-compose up -d"
    exit 1
fi

# Execute sqlite3 in the container
echo "Connecting to SQLite database: ${DB_PATH}"
echo "Type .exit or press Ctrl+D to exit the SQLite shell"
echo "---"

docker exec -it "${CONTAINER_NAME}" sqlite3 "${DB_PATH}"
