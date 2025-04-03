#!/bin/bash

# Script to set up two databases (main and alternative) with differing schemas,
# create a comparison procedure, and then run the comparison.
# Assumes MySQL server is running.
# This script can be run from any directory within the project.

# Determine the project root directory based on the script's location
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_ROOT=$( cd -- "$SCRIPT_DIR/.." &> /dev/null && pwd )

# Define paths relative to the project root
SQL_DIR="$PROJECT_ROOT/sql"
RESULTS_DIR="$PROJECT_ROOT/results/comparison"

# Define database names
DB1="park_management"
DB2="park_management_alt"

# Define MySQL connection details (adjust if necessary)
MYSQL_USER="root"

echo "--- Database Comparison Workflow ---"

# --- Step 1: Setup Main Database Schema ---
echo "Setting up main database schema ($DB1)..."
"$SCRIPT_DIR/setup_schema.sh"
if [ $? -ne 0 ]; then
  echo "ERROR: Failed to setup main schema ($DB1)."
  exit 1
fi

# --- Step 2: Setup Alternative Database Schema ---
echo "Setting up alternative database schema ($DB2)..."
# Teardown alternative DB first (setup_alternative_db.sql only creates)
echo "Attempting to teardown existing alternative database ($DB2)..."
mysql -u"$MYSQL_USER" -p -e "DROP DATABASE IF EXISTS $DB2;"
if [ $? -ne 0 ]; then
    echo "Teardown of $DB2 failed or DB didn't exist. Continuing..."
else
    echo "Teardown of $DB2 successful."
fi
# Create alternative DB
mysql -u"$MYSQL_USER" -p < "$SQL_DIR/setup_alternative_db.sql"
if [ $? -ne 0 ]; then
  echo "ERROR: Failed to setup alternative schema ($DB2)."
  exit 1
fi
echo "Alternative database schema ($DB2) setup successful."

# --- Step 3: Create Comparison Procedure ---
echo "Creating comparison stored procedure in $DB1..."
mysql -u"$MYSQL_USER" -p < "$SQL_DIR/create_comparison_procedure.sql"
if [ $? -ne 0 ]; then
  echo "ERROR: Failed to create comparison procedure."
  exit 1
fi
echo "Comparison procedure created."

# --- Step 4: Run Comparison ---
# Create results directory if it doesn't exist
mkdir -p "$RESULTS_DIR"
echo "Ensured results directory exists: $RESULTS_DIR"
COMPARISON_OUTPUT="$RESULTS_DIR/schema_comparison_output.txt"

echo "Running database schema comparison (output to $COMPARISON_OUTPUT)..."
# Execute the CALL statement, redirecting output
mysql -u"$MYSQL_USER" -p -e "CALL $DB1.compare_databases('$DB1', '$DB2');" > "$COMPARISON_OUTPUT"
if [ $? -ne 0 ]; then
  echo "ERROR: Failed to run database comparison procedure."
  exit 1
fi
echo "Database comparison complete."

echo "--- Workflow Finished ---"
echo "Comparison results saved in $COMPARISON_OUTPUT"
exit 0
