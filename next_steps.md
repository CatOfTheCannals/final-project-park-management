# Next Steps for Final Project Completion

This document outlines the remaining tasks to finalize the BBDD final project.

## 1. Populate Database with Sample Data

*   **Goal:** Add a substantial and interconnected set of artificial data to enable meaningful demonstrations and performance analysis (e.g., using `EXPLAIN` for queries).
*   **Action:**
    *   Modify the existing `sql/populate_data.sql` script.
    *   **Leverage CSV Data:** Use province names from `data/areas_protegidas_nacionales_y_provinciales_por_jurisdiccion.csv` as a base for the `provinces` table. Use species group information from `data/representatividad_de_las_especies_en_areas_protegidas_nacionales.csv` to inspire the types of `natural_elements` created. Use visitor statistics from `data/visitantes_registrados_en_los_parques_nacionales.csv` to guide the scale of visitor data. Invent park names, personnel details, accommodation specifics, etc., as required by the assignment guidelines ("invent data that is not contained in the source files").
    *   **Scale:** Aim for approximately 100 rows in major tables like `personnel`, `visitors`, `natural_elements`, and `area_elements`. Adjust counts for other tables logically (e.g., fewer `parks` than `areas`, fewer `provinces` than `parks`).
    *   **Interconnectivity:** Ensure data integrity and realistic relationships:
        *   Link `park_provinces` correctly to `parks` and `provinces`.
        *   Assign `park_areas` to existing `parks`.
        *   Place `natural_elements` within specific `park_areas` via `area_elements`.
        *   Assign `personnel` subtypes (management, surveillance, etc.) and link them to relevant entities (entrances, areas, projects).
        *   Place `visitors` in `accommodations` located within `parks`.
        *   Link `visitors` and `accommodations` to `excursions`.
        *   Create plausible `element_food` relationships between `animal_elements` and other non-mineral `natural_elements`.
    *   **Functionality:** Ensure the generated data allows for meaningful results from all required functional queries (Func Reqs 1-3, Add Reqs 3-4).
*   **Definition of Done:** `sql/populate_data.sql` is updated with ~100 interconnected rows per major table, leveraging CSV data where appropriate, and can be run after `sql/setup.sql`.

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
