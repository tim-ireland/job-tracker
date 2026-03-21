#!/bin/bash
# Start MCP server in background
echo "Starting MCP server on port ${MCP_PORT:-3000}"
job-tracker-mcp &
MCP_PID=$!

# Start uvicorn (foreground)
if [ "$UVICORN_RELOAD" = "1" ]; then
    echo "Starting API in DEVELOPMENT mode (auto-reload enabled)"
    uvicorn job_tracker.app:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Starting API in PRODUCTION mode"
    uvicorn job_tracker.app:app --host 0.0.0.0 --port 8000
fi

kill $MCP_PID 2>/dev/null
