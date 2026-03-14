#!/bin/bash
# Helper script to run the job tracker with Docker

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

# Check if data directory exists
DATA_DIR="${DATA_PATH:-../my-job-search-2026}"
if [ ! -d "$DATA_DIR" ]; then
    echo "⚠️  Data directory not found: $DATA_DIR"
    echo "📁 Creating data directory..."
    mkdir -p "$DATA_DIR"
fi

echo "🐳 Starting Job Search Toolkit..."
echo "📊 Data directory: $DATA_DIR"
echo ""

# Start with docker-compose
docker-compose up -d

echo ""
echo "✅ Job Search Toolkit is running!"
echo "🌐 Open your browser to: http://localhost:8000"
echo ""
echo "Useful commands:"
echo "  docker-compose logs -f          # View logs"
echo "  docker-compose down             # Stop application"
echo "  docker-compose exec job-tracker bash  # Open shell"
