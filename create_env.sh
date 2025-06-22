#!/usr/bin/env bash
# create_env.sh - Create a Python virtual environment (compatible with Git Bash on Windows)
set -euo pipefail

# Usage: ./create_env.sh [ENV_DIR] [PYTHON_CMD]
# ENV_DIR: directory name for the virtual environment (default: venv)
# PYTHON_CMD: python command to use (default: python3)
ENV_DIR=${1:-venv}
PYTHON_CMD=${2:-python3}

printf "Creating Python virtual environment in '%s' using '%s'...\n" "$ENV_DIR" "$PYTHON_CMD"

if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
  echo "Error: $PYTHON_CMD not found. Please install Python or specify a valid python command."
  exit 1
fi

"$PYTHON_CMD" -m venv "$ENV_DIR"
echo "Virtual environment created at $ENV_DIR."

# Determine activation script path
if [ -f "$ENV_DIR/Scripts/activate" ]; then
  ACTIVATE="$ENV_DIR/Scripts/activate"
elif [ -f "$ENV_DIR/bin/activate" ]; then
  ACTIVATE="$ENV_DIR/bin/activate"
else
  echo "Error: activation script not found in $ENV_DIR."
  exit 1
fi

# Upgrade pip in the new environment
echo "Upgrading pip inside the virtual environment..."
if [ -f "$ENV_DIR/Scripts/python" ]; then
  VENV_PYTHON="$ENV_DIR/Scripts/python"
else
  VENV_PYTHON="$ENV_DIR/bin/python"
fi

"$VENV_PYTHON" -m pip install --upgrade pip

# Install dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
  echo "Installing dependencies from requirements.txt..."
  "$VENV_PYTHON" -m pip install -r requirements.txt
fi

# Initialize .env file if missing
if [ ! -f .env ]; then
  echo "Initializing .env file..."
  if [ -f .env.example ]; then
    cp .env.example .env
    echo "Copied .env.example to .env"
  else
    cat << 'EOL' > .env
# Environment variables for this project
# Example:
# API_KEY=your_api_key
# DB_URL=sqlite:///jobs.db
EOL
    echo "Created new blank .env file. Please update with your values."
  fi
fi

echo "\nSetup complete. To activate the virtual environment, run:"
echo "  source $ACTIVATE"