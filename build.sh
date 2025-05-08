#!/bin/bash

set -e

# Default to repo name, but allow override for custom domains
REPO_NAME="static_site_generator"
BASE_PATH="/${REPO_NAME}/"

# Allow override via environment variable
if [ -n "$GITHUB_PAGES_BASE_PATH" ]; then
    BASE_PATH="$GITHUB_PAGES_BASE_PATH"
fi

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

python3 src/main.py "${BASE_PATH}"