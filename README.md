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

### 2. Running Setup, Population, Tests, and Analysis

We provide shell scripts to automate the common workflows. Ensure they are executable:
```bash
chmod +x scripts/*.sh
```

*   **Setup Database Schema:** Creates a clean, empty database structure. Handles teardown first.
    ```bash
    ./scripts/setup_schema.sh
    ```
    *(Prompts for MySQL password)*

*   **Populate Database:** Loads data from CSV files into the existing schema. Requires `local_infile` to be enabled (see Prerequisites).
    ```bash
    ./scripts/populate_database.sh
    ```
    *(Prompts for MySQL password)*

*   **Run Unit Tests:** Sets up a clean schema and runs the Python unit tests. Tests manage their own data insertion/deletion.
    ```bash
    ./scripts/run_tests.sh
    ```
    *(Prompts for MySQL password during schema setup)*

*   **Run SQL Analysis:** Sets up a clean schema, populates it with data, and then runs the SQL analysis scripts (`analyze_table_sizes.sql`, `analyze_execution_plans.sql`). Requires `local_infile`. Results are saved to files within the `results/analysis/` directory.
    ```bash
    ./scripts/run_analysis.sh
    ```
    *(Prompts for MySQL password multiple times)*

*   **Manual Execution:** If you prefer manual execution, run the SQL scripts using the `mysql` client from the project root directory:
    ```bash
    # 1. Setup Schema (Teardown is included)
    mysql -u root -p < sql/setup.sql
    
    # 2. Run Unit Tests (Against empty schema)
    python -m unittest discover tests
    
    # 3. Populate Data (Requires local_infile enabled)
    mysql --local-infile=1 -u root -p < sql/populate_data.sql
    
    # 4. Run Analysis Scripts (Requires FILE privilege)
    mysql --local-infile=1 -u root -p < sql/analyze_table_sizes.sql
    mysql --local-infile=1 -u root -p < sql/analyze_execution_plans.sql
    ```

*Note on `local_infile`: If you cannot enable `local_infile` on the server or client, you must modify `sql/populate_data.sql` to remove the `LOCAL` keyword from `LOAD DATA LOCAL INFILE` commands. This requires placing the CSV files in a directory accessible *directly* by the MySQL server process (often restricted by `secure_file_priv`).*

## Running Analysis (Standalone)

If the database is already set up and populated, you can run *only* the analysis scripts and redirect their output manually:

```bash
# Ensure you are in the project root directory
mkdir -p results/analysis # Create directory if needed
mysql --local-infile=1 -u root -p < sql/analyze_table_sizes.sql > results/analysis/table_sizes_output.txt
mysql --local-infile=1 -u root -p < sql/analyze_execution_plans.sql > results/analysis/execution_plans_output.txt
```
*(You will be prompted for the MySQL password. Results are saved to the specified files.)*

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
