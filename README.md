# Park Management Database Project

This project implements a database system for managing information about natural parks in Argentina, based on the requirements for a university assignment.

## Prerequisites

*   **Python:** Version 3.x (tested with 3.13)
*   **MySQL Server:** A running MySQL server instance (tested with 8.x). Ensure you have credentials (user/password) with privileges to create databases and tables. The default connection uses `root` with no password on `localhost`. Adjust connection details in test files if needed.
*   **Python MySQL Connector:** The `pymysql` library. Install using pip:
    ```bash
    pip install pymysql
    ```

## Database Setup

1.  **Clean up any existing database:** Before setting up, it's recommended to run the teardown script first to avoid conflicts with previous installations:
    ```bash
    # Example using mysql client (enter password when prompted)
    mysql -u root -p < sql/teardown.sql
    ```

2.  **Run Setup Script:** Execute the `setup.sql` script to create the database (`park_management`) and all necessary tables, triggers, and procedures:
    ```bash
    # Example using mysql client (enter password when prompted)
    mysql -u root -p < sql/setup.sql
    ```
    *Note: This script includes `CREATE DATABASE IF NOT EXISTS park_management;` and `USE park_management;`.*

## Populating Data (Required for Functional Tests)

To populate the database with sample data for demonstration and query testing:

1.  **Run Populate Script:** After running `setup.sql`, execute the `populate_data.sql` script:
    ```bash
    # Example using mysql client (enter password when prompted)
    mysql -u root -p < sql/populate_data.sql
    ```

## Running Tests

To verify the database schema, constraints, and functional requirements implementation:

1.  **Run Unittests:** Execute the following command from the project's root directory:
    ```bash
    python -m unittest discover tests
    ```
    All tests should pass if the database is set up correctly.

2.  **Run Individual Test Files:** If you want to run specific tests:
    ```bash
    # Example: Run only the functional requirements tests
    python -m unittest tests/test_functional_requirements.py
    
    # Example: Run only a specific data requirement test
    python -m unittest tests/test_data_requirements/test_parks.py
    ```

## Database Teardown

To remove the database created by this project:

1.  **Run Teardown Script:** Execute the `teardown.sql` script:
    ```bash
    # Example using mysql client (enter password when prompted)
    mysql -u root -p < sql/teardown.sql
    ```
    *Warning: This will permanently delete the `park_management` database and all its data.*

## Project Structure

*   `data/`: Contains original CSV data files (read-only reference).
*   `sql/`: Contains SQL scripts for setup, teardown, and data population.
*   `tests/`: Contains Python unittest files.
    *   `test_database_connection.py`: Tests basic connection and table existence.
    *   `test_data_requirements/`: Tests specific schema details and constraints for each table.
    *   `test_functional_requirements.py`: Tests the required queries and trigger functionality.
*   `guidelines.md`: Original assignment guidelines.
*   `parsed_guidelines.md`: Annotated guidelines mapping to requirements.
*   `report.md`: Project report addressing analysis requirements.
*   `specifications.txt`: Consolidated list of requirements and their status.
*   `next_steps.md`: Outline of final steps for completion.
*   `README.md`: This file.

## Troubleshooting

If you encounter errors during setup or testing:

1. **Duplicate entries or existing triggers:** Run the teardown script first, then setup again.
2. **Foreign key constraint failures:** Ensure you're running the scripts in the correct order: teardown → setup → populate.
3. **Test failures:** Check if the database was properly populated with sample data.
