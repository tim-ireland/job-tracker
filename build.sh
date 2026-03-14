#!/bin/bash
# Build script for Job Search Toolkit
# Builds the Docker image for the application

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Default values
IMAGE_NAME="${IMAGE_NAME:-job-search-toolkit}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
BUILD_ARGS=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-cache)
            BUILD_ARGS="$BUILD_ARGS --no-cache"
            shift
            ;;
        --tag)
            IMAGE_TAG="$2"
            shift 2
            ;;
        --help)
            echo "Usage: ./build.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --no-cache    Build without using cache"
            echo "  --tag TAG     Tag for the image (default: latest)"
            echo "  --help        Show this help message"
            echo ""
            echo "Environment variables:"
            echo "  IMAGE_NAME    Name of the Docker image (default: job-search-toolkit)"
            echo "  IMAGE_TAG     Tag for the image (default: latest)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "🔨 Building Job Search Toolkit Docker image..."
echo "   Image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo ""

# Build the image
docker build $BUILD_ARGS \
    -t "${IMAGE_NAME}:${IMAGE_TAG}" \
    -f Dockerfile \
    .

echo ""
echo "✅ Build complete!"
echo "   Image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo ""
echo "Next steps:"
echo "  ./run.sh              # Run in production mode"
echo "  ./run.sh --dev        # Run in development mode (live code reloading)"
echo "  ./run.sh --help       # See all run options"
