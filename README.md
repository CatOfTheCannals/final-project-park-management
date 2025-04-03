# Park Management Database Project

This project implements a database system for managing information about natural parks in Argentina, based on the requirements for an assignment at Universidad de Buenos Aires (UBA) .



## Prerequisites

*   **Python:** Version 3.x (tested with 3.13)
*   **MySQL Server:** A running MySQL server instance (tested with 8.x). Ensure you have credentials (user/password) with privileges to create databases and tables. The default connection uses `root` with no password on `localhost`. Adjust connection details in script files if needed.
*   **Python MySQL Connector:** The `pymysql` library. Install using pip:
    ```bash
    pip install pymysql
    ```

## Database Management and Workflows

This section details how to manage the `park_management` database lifecycle, including schema creation, data
population, testing, analysis, and schema comparison using the provided scripts.

### 1. Prerequisites

*   **MySQL Server:** A running MySQL server instance.
*   **MySQL Client:** The `mysql` command-line client.
*   **Python:** Version 3.x.
*   **pymysql:** Python library (`pip install pymysql`).
*   **`local_infile` Enabled (Conditional):**
    *   This setting **must** be enabled on both the MySQL server and client **only** if you intend to populate the
database using `scripts/populate_database.sh` or `scripts/run_analysis.sh` (which includes population), or if running
`sql/populate_data.sql` manually.
    *   **Server Check:** `SHOW GLOBAL VARIABLES LIKE 'local_infile';` (Should be `ON`).
    *   **Enabling:** If `OFF`, enable it in your MySQL configuration (e.g., `my.cnf`, add `local_infile=1` under
`[mysqld]`, restart server) or run `SET GLOBAL local_infile = 1;` (requires SUPER privilege, may not persist).
    *   **Client Flag:** Use the `--local-infile=1` flag when running `mysql` commands involving data population.

### 2. Automated Workflows (Recommended)

Use the provided shell scripts in the `scripts/` directory for common tasks. Ensure they are executable first:
```bash
chmod +x scripts/*.sh
```

Each script is designed to be run independently and ensures a clean state by performing necessary setup/teardown
steps.

*   **Run Unit Tests:** Sets up a clean, empty schema (runs `setup_schema.sh`) and then executes the Python unit
tests. This verifies the schema creation and basic constraints without relying on populated data.
    ```bash
    ./scripts/run_tests.sh
    ```
    *(Prompts for MySQL password during schema setup)*

*   **Run Full Analysis:** Sets up a clean schema, populates it with the full dataset from CSVs, and runs SQL analysis
scripts (`analyze_table_sizes.sql`, `analyze_execution_plans.sql`). Requires `local_infile`. Saves results to
`pre_computed_results/analysis/`. This workflow demonstrates the queries and indexing against the intended dataset.
    ```bash
    ./scripts/run_analysis.sh
    ```
    *(Prompts for MySQL password multiple times)*

*   **Run Database Schema Comparison:** Sets up the main schema, sets up an alternative schema (`park_management_alt`)
with known differences, creates the comparison procedure, runs it, and saves the output to
`pre_computed_results/comparison/`. This demonstrates the schema comparison requirement.
    ```bash
    ./scripts/run_db_comparison.sh
    ```
    *(Prompts for MySQL password multiple times)*

*   **Setup Schema Only:** Creates a clean, empty database structure (`park_management`). Automatically handles
teardown of existing `park_management` and `park_management_alt` databases. Useful for manual inspection or before
manual population.
    ```bash
    ./scripts/setup_schema.sh
    ```
    *(Prompts for MySQL password)*

*   **Populate Database Only:** Loads data from `data/load/*.csv` into the *existing* schema. Requires `local_infile`
enabled and the schema to exist (run `setup_schema.sh` first if needed).
    ```bash
    ./scripts/populate_database.sh
    ```
    *(Prompts for MySQL password)*

### 3. Manual Execution Steps

If you prefer to run steps manually from the project root:

*   **Setup Schema:**
    ```bash
    # Optional: Teardown first for a clean slate
    mysql -u root -p < sql/teardown.sql
    # Create schema
    mysql -u root -p < sql/setup.sql
    ```
*   **Populate Data:** (Requires schema and `local_infile`)
    ```bash
    mysql --local-infile=1 -u root -p < sql/populate_data.sql
    ```
*   **Run Unit Tests:** (Requires schema)
    ```bash
    python -m unittest discover tests
    ```
*   **Run Analysis Scripts:** (Requires populated schema and `local_infile`)
    ```bash
    mkdir -p pre_computed_results/analysis
    mysql --local-infile=1 -u root -p < sql/analyze_table_sizes.sql >
pre_computed_results/analysis/table_sizes_output.txt
    mysql --local-infile=1 -u root -p < sql/analyze_execution_plans.sql >
pre_computed_results/analysis/execution_plans_output.txt
    ```
*   **Run Database Comparison:** (Requires main schema)
    ```bash
    # Setup alternative DB
    mysql -u root -p -e "DROP DATABASE IF EXISTS park_management_alt;"
    mysql -u root -p < sql/setup_alternative_db.sql
    # Create procedure in main DB
    mysql -u root -p < sql/create_comparison_procedure.sql
    # Run comparison and save output
    mkdir -p pre_computed_results/comparison
    mysql -u root -p -e "CALL park_management.compare_databases('park_management', 'park_management_alt');" >
pre_computed_results/comparison/schema_comparison_output.txt
    ```

### 4. Generating ER Diagrams with ERAlchemy

This project uses [ERAlchemy](https://github.com/eralchemy/eralchemy) to automatically generate an Entity Relationship Diagram (ERD) of the `park_management` database. Follow these steps to set up and run ERAlchemy:

1. **Install Graphviz:**  
   On macOS, install Graphviz using Homebrew:
   ```bash
   brew install graphviz
   ```
   Then, ensure the build process can find Graphviz's headers and libraries by exporting the paths:
   ```bash
   export CFLAGS="-I$(brew --prefix graphviz)/include"
   export LDFLAGS="-L$(brew --prefix graphviz)/lib"
   ```

2. **Install MySQL Client Library:**  
   Since ERAlchemy uses the MySQLdb dialect, install the `mysqlclient` package:
   ```bash
   pip install mysqlclient
   ```

3. **Generate the ER Diagram:**  
   Run the following command (note that the connection string is wrapped in quotes to prevent shell interpretation of special characters):
   ```bash
   eralchemy -i 'mysql+mysqldb://root:@localhost/park_management?charset=utf8mb4' -o park_management_er.png
   ```
   To view the generated diagram, open the PNG file:
   ```bash
   open park_management_er.png
   ```


### 5. Database Teardown

To remove the databases created by this project (`park_management` and `park_management_alt`):

```bash
mysql -u root -p < sql/teardown.sql
```
*Warning: This permanently deletes the databases and all their data.*

## Troubleshooting

If you encounter errors:

1.  **Permissions/Connection Errors:** Verify MySQL server is running and credentials are correct. Check
`local_infile` settings if applicable.
2.  **Existing Objects:** Run the appropriate teardown first (`teardown.sql` or the specific setup script like
`setup_schema.sh`).
3.  **Foreign Key Errors:** Ensure scripts are run in the correct order if executing manually (setup before populate).
Automated scripts handle this.
4.  **Test Failures:** Ensure the schema is correctly set up. `run_tests.sh` handles this. If running manually, ensure
`setup.sql` succeeded.