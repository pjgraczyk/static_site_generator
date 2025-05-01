#!/bin/sh
source ./.venv/bin/activate
python3 -m unittest discover -s src -p "test_*.py" -vv
