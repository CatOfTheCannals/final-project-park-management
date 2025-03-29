#!/bin/bash

# Script to run the complete database setup, population, and analysis process
# Author: Your Name
# Date: 2025-03-29

# Set variables
MYSQL_USER="root"
MYSQL_PASS=""
MYSQL_HOST="localhost"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to execute SQL scripts
execute_sql() {
    local script=$1
    local description=$2
    
    echo -e "${YELLOW}Executing $description...${NC}"
    
    if [ -z "$MYSQL_PASS" ]; then
        mysql -u $MYSQL_USER -h $MYSQL_HOST < $script
    else
        mysql -u $MYSQL_USER -p$MYSQL_PASS -h $MYSQL_HOST < $script
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $description completed successfully${NC}"
    else
        echo -e "${RED}✗ Error executing $description${NC}"
        exit 1
    fi
}

# Create results directory if it doesn't exist
mkdir -p results
echo -e "${GREEN}✓ Created results directory${NC}"

# Step 1: Teardown any existing database
execute_sql "sql/teardown.sql" "database teardown"

# Step 2: Setup database schema
execute_sql "sql/setup.sql" "database setup"

# Step 3: Populate database with sample data
execute_sql "sql/populate_data.sql" "data population"

# Step 4: Analyze table sizes
execute_sql "sql/analyze_table_sizes.sql" "table size analysis"

# Step 5: Analyze execution plans
execute_sql "sql/analyze_execution_plans.sql" "execution plan analysis"

# Step 6: Run tests (optional)
echo -e "${YELLOW}Do you want to run the tests? (y/n)${NC}"
read run_tests

if [ "$run_tests" = "y" ] || [ "$run_tests" = "Y" ]; then
    echo -e "${YELLOW}Running tests...${NC}"
    python -m unittest discover tests
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed${NC}"
    else
        echo -e "${RED}✗ Some tests failed${NC}"
    fi
fi

echo -e "${GREEN}Analysis complete! Results are available in the 'results' directory.${NC}"
