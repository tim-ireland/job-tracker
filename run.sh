#!/bin/bash
# Run script for Job Search Toolkit
# Runs the Docker container using 12-factor app principles

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    echo "📋 Loading configuration from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Default configuration (12-factor: use environment variables)
IMAGE_NAME="${IMAGE_NAME:-job-search-toolkit}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
CONTAINER_NAME="${CONTAINER_NAME:-job-search-tracker}"
DATA_DIR="${DATA_DIR:-../my-job-search-2026}"
HOST_PORT="${HOST_PORT:-8000}"
CONTAINER_PORT="${CONTAINER_PORT:-8000}"
MCP_HOST_PORT="${MCP_HOST_PORT:-3000}"
MCP_CONTAINER_PORT="${MCP_CONTAINER_PORT:-3000}"

# Runtime configuration
DETACH=true
REMOVE=false
INTERACTIVE=false
DEV_MODE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --data-dir)
            DATA_DIR="$2"
            shift 2
            ;;
        --port)
            HOST_PORT="$2"
            shift 2
            ;;
        --mcp-port)
            MCP_HOST_PORT="$2"
            shift 2
            ;;
        --dev)
            DEV_MODE=true
            shift
            ;;
        --foreground|-f)
            DETACH=false
            shift
            ;;
        --interactive|-i)
            INTERACTIVE=true
            DETACH=false
            shift
            ;;
        --rm)
            REMOVE=true
            shift
            ;;
        --help)
            cat << EOF
Usage: ./run.sh [OPTIONS]

Run the Job Search Toolkit Docker container.

Options:
  --data-dir PATH      Path to data directory (default: ../my-job-search-2026)
  --port PORT          Host port to bind (default: 8000)
  --mcp-port PORT      Host port for MCP server (default: 3000)
  --dev                Enable development mode (live code reloading)
  --foreground, -f     Run in foreground (don't detach)
  --interactive, -i    Run interactive shell (with TTY)
  --rm                 Remove container when it exits
  --help               Show this help message

Environment Variables (12-factor configuration):
  IMAGE_NAME           Docker image name (default: job-search-toolkit)
  IMAGE_TAG            Docker image tag (default: latest)
  CONTAINER_NAME       Container name (default: job-search-tracker)
  DATA_DIR             Path to data directory (default: ../my-job-search-2026)
  HOST_PORT            Host port (default: 8000)
  DATABASE_URL         Database connection string (auto-configured)
  LOG_LEVEL            Logging level (default: info)

Configuration file:
  Create a .env file in the project root to set default values.
  See .env.example for reference.

Examples:
  ./run.sh                              # Run with defaults
  ./run.sh --dev                        # Run in development mode
  ./run.sh --data-dir ~/my-job-data     # Use custom data directory
  ./run.sh --port 8080                  # Use different port
  ./run.sh --foreground                 # Run in foreground with logs
  ./run.sh --interactive                # Open interactive shell

Data Directory:
  The data directory will be mounted at /data inside the container.
  If it doesn't exist, it will be created and initialized on first run.

Stopping:
  docker stop ${CONTAINER_NAME}
  
Logs:
  docker logs -f ${CONTAINER_NAME}
EOF
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Validate data directory exists or create it
if [ ! -d "$DATA_DIR" ]; then
    echo "⚠️  Data directory not found: $DATA_DIR"
    echo "📁 Creating data directory..."
    mkdir -p "$DATA_DIR"
fi

# Get absolute path for data directory
DATA_DIR_ABS=$(cd "$DATA_DIR" && pwd)

# Stop existing container if running
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "🛑 Stopping existing container: ${CONTAINER_NAME}"
    docker stop "${CONTAINER_NAME}" 2>/dev/null || true
    docker rm "${CONTAINER_NAME}" 2>/dev/null || true
fi

# Build docker run command
DOCKER_RUN_CMD="docker run"

# Container options
if [ "$DETACH" = true ]; then
    DOCKER_RUN_CMD="$DOCKER_RUN_CMD -d"
fi

if [ "$REMOVE" = true ]; then
    DOCKER_RUN_CMD="$DOCKER_RUN_CMD --rm"
fi

if [ "$INTERACTIVE" = true ]; then
    DOCKER_RUN_CMD="$DOCKER_RUN_CMD -it"
fi

# Name the container
DOCKER_RUN_CMD="$DOCKER_RUN_CMD --name ${CONTAINER_NAME}"

# Port mapping
DOCKER_RUN_CMD="$DOCKER_RUN_CMD -p ${HOST_PORT}:${CONTAINER_PORT}"
DOCKER_RUN_CMD="$DOCKER_RUN_CMD -p ${MCP_HOST_PORT}:${MCP_CONTAINER_PORT}"

# Volume mount
DOCKER_RUN_CMD="$DOCKER_RUN_CMD -v ${DATA_DIR_ABS}:/data"

# Development mode: mount code directories for live reloading
if [ "$DEV_MODE" = true ]; then
    SCRIPT_DIR_ABS=$(cd "$SCRIPT_DIR" && pwd)
    DOCKER_RUN_CMD="$DOCKER_RUN_CMD -v ${SCRIPT_DIR_ABS}/job_tracker:/app/job_tracker"
    DOCKER_RUN_CMD="$DOCKER_RUN_CMD -v ${SCRIPT_DIR_ABS}/templates:/app/templates"
    DOCKER_RUN_CMD="$DOCKER_RUN_CMD -v ${SCRIPT_DIR_ABS}/scripts:/app/scripts"
fi

# Environment variables (12-factor)
DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e DATA_DIR=/data"
DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e DATABASE_URL=sqlite:////data/job_applications.db"
DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e PYTHONUNBUFFERED=1"

# Enable uvicorn reload in dev mode
if [ "$DEV_MODE" = true ]; then
    DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e UVICORN_RELOAD=1"
fi

# Pass through additional environment variables if set
[ -n "$LOG_LEVEL" ] && DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e LOG_LEVEL=$LOG_LEVEL"
[ -n "$TEMPLATES_DIR" ] && DOCKER_RUN_CMD="$DOCKER_RUN_CMD -e TEMPLATES_DIR=$TEMPLATES_DIR"

# Restart policy (only if detached and not using --rm)
if [ "$DETACH" = true ] && [ "$REMOVE" = false ]; then
    DOCKER_RUN_CMD="$DOCKER_RUN_CMD --restart unless-stopped"
fi

# Health check
DOCKER_RUN_CMD="$DOCKER_RUN_CMD --health-cmd='curl -f http://localhost:${CONTAINER_PORT}/api/health || exit 1'"
DOCKER_RUN_CMD="$DOCKER_RUN_CMD --health-interval=30s"
DOCKER_RUN_CMD="$DOCKER_RUN_CMD --health-timeout=10s"
DOCKER_RUN_CMD="$DOCKER_RUN_CMD --health-retries=3"
DOCKER_RUN_CMD="$DOCKER_RUN_CMD --health-start-period=40s"

# Image
DOCKER_RUN_CMD="$DOCKER_RUN_CMD ${IMAGE_NAME}:${IMAGE_TAG}"

# Command override for interactive mode
if [ "$INTERACTIVE" = true ]; then
    DOCKER_RUN_CMD="$DOCKER_RUN_CMD /bin/bash"
fi

# Display configuration
echo "🐳 Starting Job Search Toolkit..."
echo ""
echo "Configuration:"
echo "  Image:          ${IMAGE_NAME}:${IMAGE_TAG}"
echo "  Container:      ${CONTAINER_NAME}"
echo "  Data directory: ${DATA_DIR_ABS}"
echo "  Port mapping:   ${HOST_PORT}:${CONTAINER_PORT} (app), ${MCP_HOST_PORT}:${MCP_CONTAINER_PORT} (MCP)"
echo "  Mode:           $([ "$DETACH" = true ] && echo "detached" || echo "foreground")"
if [ "$DEV_MODE" = true ]; then
    echo "  Development:    ENABLED (live code reloading)"
fi
echo ""

# Run the container
eval $DOCKER_RUN_CMD

if [ "$DETACH" = true ]; then
    echo ""
    echo "✅ Container started!"
    echo ""
    echo "🌐 Access the application:"
    echo "   http://localhost:${HOST_PORT}"
    echo ""
    echo "Useful commands:"
    echo "  docker logs -f ${CONTAINER_NAME}                 # View logs"
    echo "  docker exec -it ${CONTAINER_NAME} bash           # Open shell"
    echo "  docker exec ${CONTAINER_NAME} python scripts/sync_applications.py  # Sync apps"
    echo "  docker stop ${CONTAINER_NAME}                    # Stop container"
    echo "  docker restart ${CONTAINER_NAME}                 # Restart container"
    echo ""
elif [ "$INTERACTIVE" = false ]; then
    echo ""
    echo "✅ Container running in foreground. Press Ctrl+C to stop."
    echo ""
fi
