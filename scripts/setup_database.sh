#!/bin/bash

# Script to teardown, setup, and populate the park_management database.
# Assumes MySQL server is running and 'local_infile' is enabled on server and client.
# Run this script from the project root directory.

# Define MySQL connection details (adjust if necessary)
MYSQL_USER="root"
# Note: Using -p without a password will prompt for it securely.
# If you have a password set, you might use: MYSQL_PASSWORD="your_password" mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" ...
# However, embedding passwords in scripts is generally discouraged.

echo "Attempting to teardown existing database (if any)..."
mysql --local-infile=1 -u"$MYSQL_USER" -p < sql/teardown.sql
if [ $? -ne 0 ]; then
  echo "Teardown failed or database didn't exist. Continuing..."
else
  echo "Teardown successful."
fi

echo "Setting up database schema..."
mysql --local-infile=1 -u"$MYSQL_USER" -p < sql/setup.sql
if [ $? -ne 0 ]; then
  echo "ERROR: Database setup failed. Please check sql/setup.sql and MySQL connection."
  exit 1
fi
echo "Database schema setup successful."

echo "Populating database with sample data..."
mysql --local-infile=1 -u"$MYSQL_USER" -p < sql/populate_data.sql
if [ $? -ne 0 ]; then
  echo "ERROR: Database population failed. Please check sql/populate_data.sql, CSV files in data/load/, and MySQL permissions/local_infile setting."
  exit 1
fi
echo "Database population successful."

echo "Database setup and population complete."
exit 0
