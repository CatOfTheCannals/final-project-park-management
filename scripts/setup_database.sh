#!/bin/bash

# Script to teardown and setup the park_management database schema.
# Does NOT populate data.
# Assumes MySQL server is running.
# This script can be run from any directory within the project.

# Determine the project root directory based on the script's location
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_ROOT=$( cd -- "$SCRIPT_DIR/.." &> /dev/null && pwd )

# Define paths relative to the project root
SQL_DIR="$PROJECT_ROOT/sql"

# Define MySQL connection details (adjust if necessary)
MYSQL_USER="root"
# Note: Using -p without a password will prompt for it securely.

echo "Project Root: $PROJECT_ROOT"
echo "SQL Directory: $SQL_DIR"

# Change to project root so relative paths in SQL scripts work if needed
cd "$PROJECT_ROOT" || { echo "ERROR: Failed to change directory to $PROJECT_ROOT"; exit 1; }

echo "Attempting to teardown existing database (if any)..."
# No need for --local-infile=1 for teardown/setup
mysql -u"$MYSQL_USER" -p < "$SQL_DIR/teardown.sql"
if [ $? -ne 0 ]; then
  echo "Teardown failed or database didn't exist. Continuing..."
else
  echo "Teardown successful."
fi

echo "Setting up database schema..."
mysql -u"$MYSQL_USER" -p < "$SQL_DIR/setup.sql"
if [ $? -ne 0 ]; then
  echo "ERROR: Database schema setup failed. Please check $SQL_DIR/setup.sql and MySQL connection."
  exit 1
fi
echo "Database schema setup successful."

echo "Schema setup complete (database is empty)."
exit 0
