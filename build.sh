#!/bin/bash

set -e

REPO_NAME="static_site_generator"

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install pyproject.toml dependencies
# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

python3 src/main.py "/${REPO_NAME}/"