#!/bin/bash
# Martian AI Docker Startup Script
# Usage: ./docker-start.sh [options]
# Options:
#   -b, --build    Force rebuild of images
#   -d, --detach   Run in background
#   -c, --clean    Remove all containers and volumes before starting
#   -h, --help     Show this help message

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
BUILD=false
DETACH=false
CLEAN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -b|--build)
            BUILD=true
            shift
            ;;
        -d|--detach)
            DETACH=true
            shift
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        -h|--help)
            echo "Martian AI Docker Startup Script"
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  -b, --build    Force rebuild of images"
            echo "  -d, --detach   Run in background"
            echo "  -c, --clean    Remove all containers and volumes before starting"
            echo "  -h, --help     Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Function to print status messages
write_status() {
    local message=$1
    local color=$2
    echo -e "$(date '+[%H:%M:%S]') ${color}${message}${NC}"
}

# Check if Docker is installed
write_status "Checking Docker installation..." "$BLUE"
if ! command -v docker &> /dev/null; then
    write_status "✗ Docker is not installed or not in PATH" "$RED"
    echo "Please install Docker from https://www.docker.com/get-started"
    exit 1
fi
DOCKER_VERSION=$(docker --version)
write_status "✓ Docker found: $DOCKER_VERSION" "$GREEN"

# Check if docker-compose is installed
write_status "Checking Docker Compose..." "$BLUE"
if ! command -v docker-compose &> /dev/null; then
    write_status "✗ Docker Compose is not installed" "$RED"
    echo "Please ensure Docker includes Docker Compose"
    exit 1
fi
COMPOSE_VERSION=$(docker-compose --version)
write_status "✓ Docker Compose found: $COMPOSE_VERSION" "$GREEN"

# Clean if requested
if [ "$CLEAN" = true ]; then
    write_status "Cleaning up Docker resources..." "$YELLOW"
    docker-compose down -v
    if [ $? -ne 0 ]; then
        write_status "Warning: Cleanup encountered issues" "$YELLOW"
    else
        write_status "✓ Cleanup complete" "$GREEN"
    fi
fi

# Build if requested
if [ "$BUILD" = true ] || [ "$CLEAN" = true ]; then
    write_status "Building Docker images..." "$YELLOW"
    docker-compose build
    if [ $? -ne 0 ]; then
        write_status "✗ Build failed" "$RED"
        exit 1
    fi
    write_status "✓ Build successful" "$GREEN"
fi

# Start containers
write_status "Starting Martian AI..." "$YELLOW"
if [ "$DETACH" = true ]; then
    docker-compose up -d
else
    docker-compose up
fi

if [ $? -ne 0 ]; then
    write_status "✗ Failed to start containers" "$RED"
    exit 1
fi

if [ "$DETACH" = true ]; then
    write_status "✓ Containers started in background" "$GREEN"
    echo ""
    write_status "Services running:" "$BLUE"
    echo "  • Frontend: http://localhost:3000"
    echo "  • Backend API: http://localhost:8000"
    echo "  • API Docs: http://localhost:8000/docs"
    echo ""
    write_status "To view logs: docker-compose logs -f"
    write_status "To stop: docker-compose down"
else
    write_status "✓ Martian AI is running" "$GREEN"
    echo ""
    write_status "Access:" "$BLUE"
    echo "  • Frontend: http://localhost:3000"
    echo "  • Backend API: http://localhost:8000"
    echo "  • API Docs: http://localhost:8000/docs"
    echo ""
    write_status "Press Ctrl+C to stop"
fi
