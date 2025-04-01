#!/bin/bash

# Script to run Python unit tests.
# Assumes it's run from the project root directory or the script correctly finds the root.

# Determine the project root directory based on the script's location
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_ROOT=$( cd -- "$SCRIPT_DIR/.." &> /dev/null && pwd )

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
