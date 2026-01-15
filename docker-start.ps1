#!/usr/bin/env pwsh
<#
.SYNOPSIS
Martian AI Docker Startup Script

.DESCRIPTION
Builds and starts the Martian AI application with Docker Compose

.PARAMETER Build
Force rebuild of images

.PARAMETER Detach
Run in background

.PARAMETER Clean
Remove all containers and volumes before starting

.EXAMPLE
./docker-start.ps1
./docker-start.ps1 -Build
./docker-start.ps1 -Clean -Build -Detach
#>

param(
    [switch]$Build,
    [switch]$Detach,
    [switch]$Clean
)

# Colors for output
$Green = [System.ConsoleColor]::Green
$Yellow = [System.ConsoleColor]::Yellow
$Red = [System.ConsoleColor]::Red
$Blue = [System.ConsoleColor]::Blue

function Write-Status {
    param([string]$Message, [System.ConsoleColor]$Color = $Green)
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] " -ForegroundColor $Blue -NoNewline
    Write-Host $Message -ForegroundColor $Color
}

# Check if Docker is installed
Write-Status "Checking Docker installation..."
try {
    $dockerVersion = docker --version 2>$null
    if (-not $?) {
        throw "Docker not found"
    }
    Write-Status "✓ Docker found: $dockerVersion" $Green
}
catch {
    Write-Status "✗ Docker is not installed or not in PATH" $Red
    Write-Host "Please install Docker from https://www.docker.com/get-started"
    exit 1
}

# Check if docker-compose is installed
Write-Status "Checking Docker Compose..."
try {
    $composeVersion = docker-compose --version 2>$null
    if (-not $?) {
        throw "Docker Compose not found"
    }
    Write-Status "✓ Docker Compose found: $composeVersion" $Green
}
catch {
    Write-Status "✗ Docker Compose is not installed" $Red
    Write-Host "Please ensure Docker Desktop includes Docker Compose"
    exit 1
}

# Clean if requested
if ($Clean) {
    Write-Status "Cleaning up Docker resources..." $Yellow
    docker-compose down -v
    if ($LASTEXITCODE -ne 0) {
        Write-Status "Warning: Cleanup encountered issues" $Yellow
    }
    else {
        Write-Status "✓ Cleanup complete" $Green
    }
}

# Build if requested
if ($Build -or $Clean) {
    Write-Status "Building Docker images..." $Yellow
    docker-compose build
    if ($LASTEXITCODE -ne 0) {
        Write-Status "✗ Build failed" $Red
        exit 1
    }
    Write-Status "✓ Build successful" $Green
}

# Start containers
$args_str = @()
if ($Detach) {
    $args_str += "-d"
}

Write-Status "Starting Martian AI..." $Yellow
docker-compose up $args_str

if ($LASTEXITCODE -ne 0) {
    Write-Status "✗ Failed to start containers" $Red
    exit 1
}

if ($Detach) {
    Write-Status "✓ Containers started in background" $Green
    Write-Host ""
    Write-Status "Services running:" $Blue
    Write-Host "  • Frontend: http://localhost:3000"
    Write-Host "  • Backend API: http://localhost:8000"
    Write-Host "  • API Docs: http://localhost:8000/docs"
    Write-Host ""
    Write-Status "To view logs: docker-compose logs -f"
    Write-Status "To stop: docker-compose down"
}
else {
    Write-Status "✓ Martian AI is running" $Green
    Write-Host ""
    Write-Status "Access:" $Blue
    Write-Host "  • Frontend: http://localhost:3000"
    Write-Host "  • Backend API: http://localhost:8000"
    Write-Host "  • API Docs: http://localhost:8000/docs"
    Write-Host ""
    Write-Status "Press Ctrl+C to stop"
}
