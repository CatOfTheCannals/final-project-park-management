-- Create the stored procedure for comparing database schemas.
-- This should be run against the primary database (e.g., park_management)
-- after the schema has been created.

USE park_management; -- Ensure procedure is created in the main database

DELIMITER //

DROP PROCEDURE IF EXISTS compare_databases; -- Drop if it exists from previous runs

CREATE PROCEDURE compare_databases (IN db1_name VARCHAR(64), IN db2_name VARCHAR(64))
BEGIN
    SELECT 'Comparing database schemas:', db1_name, 'vs', db2_name;

    -- Compare Tables
    SELECT '-- Tables present only in ', db1_name, ' --' AS ' ';
    SELECT t1.table_name
    FROM information_schema.tables t1
    LEFT JOIN information_schema.tables t2 ON t1.table_name = t2.table_name AND t2.table_schema = db2_name
    WHERE t1.table_schema = db1_name AND t1.table_type = 'BASE TABLE' AND t2.table_name IS NULL;

    SELECT '-- Tables present only in ', db2_name, ' --' AS ' ';
    SELECT t2.table_name
    FROM information_schema.tables t2
    LEFT JOIN information_schema.tables t1 ON t1.table_name = t2.table_name AND t1.table_schema = db1_name
    WHERE t2.table_schema = db2_name AND t2.table_type = 'BASE TABLE' AND t1.table_name IS NULL;

    -- Compare Indexes (Existence on common tables)
    SELECT '-- Indexes present only in ', db1_name, ' (on common tables) --' AS ' ';
    SELECT i1.table_name, i1.index_name
    FROM information_schema.statistics i1
    LEFT JOIN information_schema.statistics i2 ON i1.table_name = i2.table_name AND i1.index_name = i2.index_name AND i2.table_schema = db2_name
    WHERE i1.table_schema = db1_name
      AND i1.table_name IN (SELECT table_name FROM information_schema.tables WHERE table_schema = db2_name AND table_type = 'BASE TABLE') -- Only compare common tables
      AND i2.index_name IS NULL;

    SELECT '-- Indexes present only in ', db2_name, ' (on common tables) --' AS ' ';
    SELECT i2.table_name, i2.index_name
    FROM information_schema.statistics i2
    LEFT JOIN information_schema.statistics i1 ON i1.table_name = i2.table_name AND i1.index_name = i2.index_name AND i1.table_schema = db1_name
    WHERE i2.table_schema = db2_name
      AND i2.table_name IN (SELECT table_name FROM information_schema.tables WHERE table_schema = db1_name AND table_type = 'BASE TABLE') -- Only compare common tables
      AND i1.index_name IS NULL;

    -- Compare Constraints (Existence on common tables)
    SELECT '-- Constraints present only in ', db1_name, ' (on common tables) --' AS ' ';
    SELECT c1.table_name, c1.constraint_name, c1.constraint_type
    FROM information_schema.table_constraints c1
    LEFT JOIN information_schema.table_constraints c2 ON c1.table_name = c2.table_name AND c1.constraint_name = c2.constraint_name AND c2.constraint_schema = db2_name
    WHERE c1.constraint_schema = db1_name
      AND c1.table_name IN (SELECT table_name FROM information_schema.tables WHERE table_schema = db2_name AND table_type = 'BASE TABLE') -- Common tables
      AND c2.constraint_name IS NULL;

    SELECT '-- Constraints present only in ', db2_name, ' (on common tables) --' AS ' ';
    SELECT c2.table_name, c2.constraint_name, c2.constraint_type
    FROM information_schema.table_constraints c2
    LEFT JOIN information_schema.table_constraints c1 ON c1.table_name = c2.table_name AND c1.constraint_name = c2.constraint_name AND c1.constraint_schema = db1_name
    WHERE c2.constraint_schema = db2_name
      AND c2.table_name IN (SELECT table_name FROM information_schema.tables WHERE table_schema = db1_name AND table_type = 'BASE TABLE') -- Common tables
      AND c1.constraint_name IS NULL;

    -- Note: Deeper comparison (e.g., index columns, constraint definitions) would require more complex queries joining multiple INFORMATION_SCHEMA tables.
    -- This implementation focuses on existence checks as required by the prompt.

    SELECT '-- Comparison Complete --' AS ' ';

END //

DELIMITER ;

SELECT 'Stored procedure compare_databases created successfully.' as status;
