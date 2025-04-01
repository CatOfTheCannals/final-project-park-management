#!/bin/bash

# Script to setup schema, populate data, and run SQL analysis scripts.
# Ensures analysis runs against a fully populated database.
# Assumes MySQL server is running and 'local_infile' is enabled.
# This script can be run from any directory within the project.
# Output files will be created in /tmp/

# Determine the project root directory based on the script's location
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_ROOT=$( cd -- "$SCRIPT_DIR/.." &> /dev/null && pwd )

# Define paths relative to the project root
SQL_DIR="$PROJECT_ROOT/sql"

# Define MySQL connection details (adjust if necessary)
MYSQL_USER="root"

echo "Setting up clean database schema for analysis..."
"$SCRIPT_DIR/setup_schema.sh" # Run the schema setup script
if [ $? -ne 0 ]; then
  echo "ERROR: Failed to setup schema before populating for analysis."
  exit 1
fi

echo "Populating database for analysis..."
"$SCRIPT_DIR/populate_database.sh" # Run the population script
if [ $? -ne 0 ]; then
  echo "ERROR: Failed to populate database before running analysis."
  exit 1
fi

echo "Changing to project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT" || { echo "ERROR: Failed to change directory to $PROJECT_ROOT"; exit 1; }

echo "Running table size analysis..."
# Use --local-infile=1 for consistency, although likely not strictly needed for INTO OUTFILE
# unless secure_file_priv is restrictive. The main requirement is FILE privilege.
mysql --local-infile=1 -u"$MYSQL_USER" -p < "$SQL_DIR/analyze_table_sizes.sql"
if [ $? -ne 0 ]; then
  echo "ERROR: Table size analysis failed. Check $SQL_DIR/analyze_table_sizes.sql and MySQL permissions (FILE privilege)."
  # Continue to next script even if this one fails
fi
echo "Table size analysis complete. Check files in /tmp/ (table_sizes.txt, etc.)."


echo "Running execution plan analysis..."
mysql --local-infile=1 -u"$MYSQL_USER" -p < "$SQL_DIR/analyze_execution_plans.sql"
if [ $? -ne 0 ]; then
  echo "ERROR: Execution plan analysis failed. Check $SQL_DIR/analyze_execution_plans.sql and MySQL permissions (FILE privilege)."
  exit 1 # Exit if this critical analysis fails
fi
echo "Execution plan analysis complete. Check files in /tmp/ (fr1_plan.json, etc.)."

echo "Analysis scripts finished."
exit 0
