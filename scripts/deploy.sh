#!/bin/bash
# Simple deployment script for the Reward Personalization Agent

echo "Deploying Reward Personalization Agent..."

# Ensure virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "Running tests..."
pytest

# Check if tests passed
if [ $? -ne 0 ]; then
    echo "Tests failed! Deployment aborted."
    exit 1
fi

# Build Docker image if Dockerfile exists
if [ -f "Dockerfile" ]; then
    echo "Building Docker image..."
    docker build -t reward-personalization-agent:latest .
fi

echo "Deployment complete!"
