#!/bin/sh
source ./.venv/bin/activate
uv sync
python3 -m unittest discover -s src -p "test_*.py" -v
