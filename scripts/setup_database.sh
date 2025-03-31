#!/bin/bash

# Script to teardown, setup, and populate the park_management database.
# Assumes MySQL server is running and 'local_infile' is enabled on server and client.
# This script can be run from any directory within the project.

# Determine the project root directory based on the script's location
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_ROOT=$( cd -- "$SCRIPT_DIR/.." &> /dev/null && pwd )

# Define paths relative to the project root
SQL_DIR="$PROJECT_ROOT/sql"
DATA_DIR="$PROJECT_ROOT/data" # Needed if populate script uses relative paths internally

# Define MySQL connection details (adjust if necessary)
MYSQL_USER="root"
# Note: Using -p without a password will prompt for it securely.
# If you have a password set, you might use: MYSQL_PASSWORD="your_password" mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" ...
# However, embedding passwords in scripts is generally discouraged.

echo "Project Root: $PROJECT_ROOT"
echo "SQL Directory: $SQL_DIR"

# Change to project root so relative paths in SQL scripts (like LOAD DATA) work
cd "$PROJECT_ROOT" || { echo "ERROR: Failed to change directory to $PROJECT_ROOT"; exit 1; }

echo "Attempting to teardown existing database (if any)..."
mysql --local-infile=1 -u"$MYSQL_USER" -p < "$SQL_DIR/teardown.sql"
if [ $? -ne 0 ]; then
  echo "Teardown failed or database didn't exist. Continuing..."
else
  echo "Teardown successful."
fi

echo "Setting up database schema..."
mysql --local-infile=1 -u"$MYSQL_USER" -p < "$SQL_DIR/setup.sql"
if [ $? -ne 0 ]; then
  echo "ERROR: Database setup failed. Please check $SQL_DIR/setup.sql and MySQL connection."
  exit 1
fi
echo "Database schema setup successful."

echo "Populating database with sample data..."
# The populate_data.sql script now uses relative paths like 'data/load/...'
# which works because we changed the current directory to PROJECT_ROOT
mysql --local-infile=1 -u"$MYSQL_USER" -p < "$SQL_DIR/populate_data.sql"
if [ $? -ne 0 ]; then
  echo "ERROR: Database population failed. Please check $SQL_DIR/populate_data.sql, CSV files in data/load/, and MySQL permissions/local_infile setting."
  exit 1
fi
echo "Database population successful."

echo "Database setup and population complete."
exit 0
