# Park Management Database Project

This project implements a database system for managing information about natural parks in Argentina, based on the requirements for a university assignment.

## Prerequisites

*   **Python:** Version 3.x (tested with 3.13)
*   **MySQL Server:** A running MySQL server instance (tested with 8.x). Ensure you have credentials (user/password) with privileges to create databases and tables. The default connection uses `root` with no password on `localhost`. Adjust connection details in test files if needed.
*   **Python MySQL Connector:** The `pymysql` library. Install using pip:
    ```bash
    pip install pymysql
    ```

## Database Setup and Population

This section details how to set up the `park_management` database, create the schema, and populate it with sample data using the provided SQL scripts and CSV files.

### 1. Prerequisites: MySQL `local_infile` Configuration

The `sql/populate_data.sql` script uses `LOAD DATA LOCAL INFILE` for efficient bulk loading from CSV files. This feature must be enabled on **both** the MySQL server and the client you use to connect.

**a) Server Configuration:**

*   **Check Current Setting:** Connect to your MySQL server as an administrator (e.g., `root`) and run:
    ```sql
    SHOW GLOBAL VARIABLES LIKE 'local_infile';
    ```
*   **Enable if `OFF`:** If the value is `OFF`, you need to enable it. The method depends on your operating system and MySQL installation:
    *   **Linux:** Edit the MySQL configuration file (e.g., `/etc/mysql/my.cnf`, `/etc/mysql/mysql.conf.d/mysqld.cnf`, or `/etc/my.cnf`). Under the `[mysqld]` section, add or modify the line:
        ```ini
        [mysqld]
        local_infile=1
        ```
        Then, restart the MySQL server: `sudo systemctl restart mysql` (or `mysqld`).
    *   **macOS (Homebrew):** Find your configuration file (often `/opt/homebrew/etc/my.cnf`). If it doesn't exist, create it. Add the following lines:
        ```ini
        [mysqld]
        local_infile=1
        ```
        Restart the MySQL server: `brew services restart mysql`.
    *   **Dynamic (Requires SUPER privilege):** You can also try setting it dynamically (this might not persist across server restarts):
        ```sql
        SET GLOBAL local_infile = 1;
        ```
*   **Verify:** Run `SHOW GLOBAL VARIABLES LIKE 'local_infile';` again. The value should now be `ON`.

**b) Client Configuration:**

*   When running the `mysql` command-line client to execute the SQL scripts, you **must** include the `--local-infile=1` flag.

### 2. Running the Setup and Population Scripts

The recommended way to set up and populate the database is using the provided shell script. This ensures the scripts are run in the correct order.

*   **Using the Script (Recommended):**
    1.  Make the script executable (if you haven't already):
        ```bash
        chmod +x scripts/setup_database.sh
        ```
    2.  Run the script from the project's root directory:
        ```bash
        ./scripts/setup_database.sh
        ```
        You might be prompted for your MySQL root password multiple times.

*   **Manual Execution:** If you prefer to run the commands manually, execute them from the project's root directory in this specific order:
    ```bash
    # 1. Teardown (Optional but recommended for a clean slate)
    mysql --local-infile=1 -u root -p < sql/teardown.sql 
    
    # 2. Setup Schema
    mysql --local-infile=1 -u root -p < sql/setup.sql
    
    # 3. Populate Data
    mysql --local-infile=1 -u root -p < sql/populate_data.sql
    ```
    *(Enter your MySQL root password when prompted for each command)*

*Note: If you cannot enable `local_infile` on the server or client, you would need to modify `sql/populate_data.sql` to remove the `LOCAL` keyword from `LOAD DATA LOCAL INFILE` commands. This requires placing the CSV files in a directory accessible *directly* by the MySQL server process, which is often restricted by the `secure_file_priv` system variable and generally less convenient for development.*

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
*   `data/load/`: Contains CSV files used to populate the database with mock data.
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
