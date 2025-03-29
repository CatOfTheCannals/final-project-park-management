# Next Steps for Final Project Completion

This document outlines the remaining tasks to finalize the BBDD final project.

## 1. Populate Database with Sample Data

*   **Goal:** Add a small but representative set of artificial data beyond the minimal test setup data. This helps in demonstrating functionality and performing basic performance analysis (e.g., using `EXPLAIN` for queries).
*   **Action:**
    *   Create a new file `sql/populate_data.sql`.
    *   Add `INSERT` statements for key tables like `provinces`, `parks`, `park_provinces`, `park_areas`, `natural_elements`, `vegetal_elements`, `animal_elements`, `area_elements`, `personnel`, `visitors`, `accommodations`, `excursions`, etc. Aim for ~5-10 realistic entries per table where applicable. Use data inspired by, but distinct from, the `data/*.csv` files.
    *   Ensure the data allows for meaningful results from the required functional queries.
*   **Definition of Done:** `sql/populate_data.sql` exists and can be run after `sql/setup.sql` to populate the database with sample data.

## 2. Create README Documentation

*   **Goal:** Provide clear instructions for setting up and running the project.
*   **Action:**
    *   Create a `README.md` file in the project root.
    *   Include sections for:
        *   **Prerequisites:** List necessary software (e.g., Python 3.x, MySQL server, `pymysql` library).
        *   **Database Setup:** Explain how to create the database user (if needed) and the database itself. Provide example commands to run `sql/setup.sql`.
        *   **Populating Data:** Provide example command to run `sql/populate_data.sql`.
        *   **Running Tests:** Provide the command `python -m unittest discover tests`.
        *   **Database Teardown:** Provide example command to run `sql/teardown.sql`.
*   **Definition of Done:** `README.md` exists with clear, actionable instructions.

## 3. Finalize Report (`report.md`)

*   **Goal:** Ensure the report addresses all requirements, especially the analysis points from the "Requisitos previos".
*   **Action:**
    *   Review `specifications.txt` and `parsed_guidelines.md` against `report.md`.
    *   Add/Expand sections covering:
        *   **Table Size Estimation (Additional Req 2):** Provide a brief estimation based on the schema and potential data volumes (e.g., number of parks, average species per park).
        *   **Index Proposal & Execution Plan Analysis (Additional Req 5):**
            *   Identify key queries (Functional Reqs 1-3, Additional Reqs 3-4).
            *   Propose suitable indexes (e.g., on foreign keys, columns used in WHERE/JOIN/ORDER BY clauses like `parks.code`, `provinces.id`, `area_elements.park_id`, `natural_elements.id`).
            *   Briefly discuss *why* these indexes are proposed.
            *   Optionally, include `EXPLAIN` output for the key queries run against the populated database (before/after adding indexes if feasible).
        *   **Database Comparison Procedure (Additional Req 6):** Mention the `compare_databases` stored procedure created in `sql/setup.sql` and its purpose.
        *   **Concurrency Control & Recovery (Additional Req 7):** Research and write a comparison of mechanisms in MySQL (InnoDB) and another commercial engine (e.g., PostgreSQL or SQL Server), focusing on technical aspects (locking mechanisms, transaction isolation levels, logging, recovery methods).
*   **Definition of Done:** `report.md` contains sections addressing all specified requirements, including the analysis points.

## 4. Final Review

*   **Goal:** Perform a final check of all components.
*   **Action:**
    *   Ensure all tests pass (`python -m unittest discover tests`).
    *   Verify that `sql/setup.sql` and `sql/populate_data.sql` run without errors.
    *   Read through `README.md` and `report.md` for clarity and completeness.
    *   Confirm all deliverables mentioned in the original guidelines (`guidelines.md`) are present or addressed.
*   **Definition of Done:** Project is ready for submission.
