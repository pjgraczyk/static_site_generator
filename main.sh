#!/bin/sh
if [ -d ".venv" ]; then
    source .venv/bin/activate
    uv sync
else
    echo "Virtual environment not found. Creating with uv..."
    uv venv .venv
    uv sync
    source .venv/bin/activate
fi
python src/main.py

cd docs
exec python -m http.server 8888
