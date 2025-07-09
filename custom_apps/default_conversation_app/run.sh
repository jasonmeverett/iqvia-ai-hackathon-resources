#!/usr/bin/env bash

echo "Starting the custom app - shell script"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR

PYTHONUNBUFFERED=1 uv run python main.py