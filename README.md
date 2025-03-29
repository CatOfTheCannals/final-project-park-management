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

1.  **Connect to MySQL:** Open a MySQL client connected to your server.
    ```bash
    # Example using mysql client (replace 'root' if using a different user)
    mysql -u root -p
    ```
2.  **Run Setup Script:** Execute the `setup.sql` script to create the database (`park_management`) and all necessary tables, triggers, and procedures. Run this from the project's root directory.
    ```bash
    # Example using mysql client (enter password when prompted)
    mysql -u root -p < sql/setup.sql
    ```
    *Note: This script includes `CREATE DATABASE IF NOT EXISTS park_management;` and `USE park_management;`.*

## Populating Data (Optional but Recommended)

To populate the database with sample data for demonstration and query testing:

1.  **Run Populate Script:** After running `setup.sql`, execute the `populate_data.sql` script.
    ```bash
    # Example using mysql client (enter password when prompted)
    mysql -u root -p park_management < sql/populate_data.sql
    ```
    *Note: We specify the database name here because `populate_data.sql` assumes the database context is already set.*

## Running Tests

To verify the database schema, constraints, and functional requirements implementation:

1.  **Run Unittests:** Execute the following command from the project's root directory:
    ```bash
    python -m unittest discover tests
    ```
    All tests should pass if the database is set up correctly.

## Database Teardown

To remove the database created by this project:

1.  **Run Teardown Script:** Execute the `teardown.sql` script.
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
