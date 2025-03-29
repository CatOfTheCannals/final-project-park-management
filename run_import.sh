#!/bin/bash

# Script to parse CSV files and import data into the database
# Author: Your Name
# Date: 2023-06-01

# Set variables
MYSQL_USER="root"
MYSQL_PASS=""
MYSQL_HOST="localhost"
MYSQL_DB="park_management"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting data import process...${NC}"

# Create import directory if it doesn't exist
mkdir -p data/import
echo -e "${GREEN}✓ Created data/import directory${NC}"

# Run the Python parser script
echo -e "${YELLOW}Parsing CSV files...${NC}"
python3 data/import/parse_csv_data.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ CSV files parsed successfully${NC}"
else
    echo -e "${RED}✗ Error parsing CSV files${NC}"
    exit 1
fi

# Run the SQL import script
echo -e "${YELLOW}Importing data into database...${NC}"
if [ -z "$MYSQL_PASS" ]; then
    mysql -u $MYSQL_USER -h $MYSQL_HOST $MYSQL_DB < sql/populate_data.sql
else
    mysql -u $MYSQL_USER -p$MYSQL_PASS -h $MYSQL_HOST $MYSQL_DB < sql/populate_data.sql
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Data imported successfully${NC}"
else
    echo -e "${RED}✗ Error importing data${NC}"
    exit 1
fi

echo -e "${GREEN}Data import process completed!${NC}"
