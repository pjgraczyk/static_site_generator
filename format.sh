#!/bin/bash

if command -v uv &> /dev/null; then
    uvx ruff format .
fi