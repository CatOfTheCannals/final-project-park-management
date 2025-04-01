#!/bin/bash

# Script to setup the schema and run Python unit tests.
# Ensures tests run against a clean, empty schema.
# Assumes MySQL server is running.
# This script can be run from any directory within the project.

# Determine the project root directory based on the script's location
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_ROOT=$( cd -- "$SCRIPT_DIR/.." &> /dev/null && pwd )

echo "Setting up clean database schema for tests..."
"$SCRIPT_DIR/setup_schema.sh" # Run the schema setup script
if [ $? -ne 0 ]; then
  echo "ERROR: Failed to setup schema before running tests."
  exit 1
fi

echo "Changing to project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT" || { echo "ERROR: Failed to change directory to $PROJECT_ROOT"; exit 1; }

echo "Running Python unit tests..."
python -m unittest discover tests

# Capture the exit code of the tests
TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -eq 0 ]; then
  echo "All tests passed."
else
  echo "ERROR: Some tests failed."
fi

exit $TEST_EXIT_CODE
