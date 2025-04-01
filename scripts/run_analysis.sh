#!/bin/bash

# Script to setup schema, populate data, and run SQL analysis scripts.
# Ensures analysis runs against a fully populated database.
# Assumes MySQL server is running and 'local_infile' is enabled.
# This script can be run from any directory within the project.
# Analysis results are printed to standard output.

# Determine the project root directory based on the script's location
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_ROOT=$( cd -- "$SCRIPT_DIR/.." &> /dev/null && pwd )

# Define paths relative to the project root
SQL_DIR="$PROJECT_ROOT/sql"
RESULTS_DIR="$PROJECT_ROOT/results/analysis"

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

# Create results directory if it doesn't exist
mkdir -p "$RESULTS_DIR"
echo "Ensured results directory exists: $RESULTS_DIR"

# Define output file paths
TABLE_SIZE_OUTPUT="$RESULTS_DIR/table_sizes_output.txt"
EXEC_PLAN_OUTPUT="$RESULTS_DIR/execution_plans_output.txt"

echo "Running table size analysis (output to $TABLE_SIZE_OUTPUT)..."
# Use --local-infile=1 for consistency. Redirect output to file.
mysql --local-infile=1 -u"$MYSQL_USER" -p < "$SQL_DIR/analyze_table_sizes.sql" > "$TABLE_SIZE_OUTPUT"
if [ $? -ne 0 ]; then
  echo "ERROR: Table size analysis failed. Check $SQL_DIR/analyze_table_sizes.sql and MySQL permissions."
  # Continue to next script even if this one fails
fi
echo "Table size analysis complete."


echo "Running execution plan analysis (output to $EXEC_PLAN_OUTPUT)..."
mysql --local-infile=1 -u"$MYSQL_USER" -p < "$SQL_DIR/analyze_execution_plans.sql" > "$EXEC_PLAN_OUTPUT"
if [ $? -ne 0 ]; then
  echo "ERROR: Execution plan analysis failed. Check $SQL_DIR/analyze_execution_plans.sql and MySQL permissions."
  exit 1 # Exit if this critical analysis fails
fi
echo "Execution plan analysis complete."

echo "Analysis scripts finished. Results saved in $RESULTS_DIR"
exit 0
