#!/bin/bash

# Script to populate the park_management database with sample data from CSVs.
# Assumes the database schema already exists (run setup_schema.sh first).
# Assumes MySQL server is running and 'local_infile' is enabled on server and client.
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

# Change to project root so relative paths in SQL scripts (like LOAD DATA) work
cd "$PROJECT_ROOT" || { echo "ERROR: Failed to change directory to $PROJECT_ROOT"; exit 1; }

echo "Populating database with sample data..."
# The populate_data.sql script uses relative paths like 'data/load/...'
# which works because we changed the current directory to PROJECT_ROOT
mysql --local-infile=1 -u"$MYSQL_USER" -p < "$SQL_DIR/populate_data.sql"
if [ $? -ne 0 ]; then
  echo "ERROR: Database population failed. Please check $SQL_DIR/populate_data.sql, CSV files in data/load/, and MySQL permissions/local_infile setting."
  exit 1
fi
echo "Database population successful."

exit 0
