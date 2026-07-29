#!/bin/bash

# Define project path (defaults to current directory if not set)
PROJECT_DIR=$PWD

echo "=========================================="
echo " Restarting Flask App in Phusion Passenger"
echo " Location: $PROJECT_DIR"
echo "=========================================="

# 1. Kill lingering Python and Passenger worker processes
echo "[1/4] Terminating existing Python & Passenger processes..."
pkill -9 -f "passenger" 2>/dev/null
pkill -9 -f "python" 2>/dev/null

# 2. Clean up compiled Python bytecode / cache files
echo "[2/4] Clearing __pycache__ and temp files..."
find "$PROJECT_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find "$PROJECT_DIR" -type f -name "*.pyc" -delete 2>/dev/null

# 3. Ensure the tmp directory exists
echo "[3/4] Preparing restart trigger directory..."
mkdir -p "$PROJECT_DIR/tmp"

# 4. Touch restart.txt to signal Phusion Passenger to reload
echo "[4/4] Touching tmp/restart.txt..."
touch "$PROJECT_DIR/tmp/restart.txt"

echo "=========================================="
echo " Done! Refresh your browser now."
echo "=========================================="
