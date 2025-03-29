-- Script to analyze table sizes in the park_management database
-- Outputs results to files for better analysis
USE park_management;

-- Create results directory if it doesn't exist
-- Note: MySQL user needs FILE privilege and write access to this directory
SET @results_dir = './results';

-- Get table sizes in MB
SELECT 
    table_name AS 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 4) AS 'Size (MB)',
    ROUND((data_length / 1024 / 1024), 4) AS 'Data Size (MB)',
    ROUND((index_length / 1024 / 1024), 4) AS 'Index Size (MB)',
    table_rows AS 'Rows'
FROM 
    information_schema.TABLES
WHERE 
    table_schema = 'park_management'
ORDER BY 
    (data_length + index_length) DESC
INTO OUTFILE './results/table_sizes.txt';

-- Get detailed information about each table
SELECT 
    CONCAT('Table: ', table_name) AS 'Table Information'
FROM 
    information_schema.TABLES
WHERE 
    table_schema = 'park_management'
ORDER BY 
    table_name
INTO OUTFILE './results/table_list.txt';

-- Count rows in each table
SELECT 'provinces' AS 'Table', COUNT(*) AS 'Row Count' FROM provinces
UNION ALL
SELECT 'parks', COUNT(*) FROM parks
UNION ALL
SELECT 'park_provinces', COUNT(*) FROM park_provinces
UNION ALL
SELECT 'park_areas', COUNT(*) FROM park_areas
UNION ALL
SELECT 'natural_elements', COUNT(*) FROM natural_elements
UNION ALL
SELECT 'vegetal_elements', COUNT(*) FROM vegetal_elements
UNION ALL
SELECT 'animal_elements', COUNT(*) FROM animal_elements
UNION ALL
SELECT 'mineral_elements', COUNT(*) FROM mineral_elements
UNION ALL
SELECT 'area_elements', COUNT(*) FROM area_elements
UNION ALL
SELECT 'element_food', COUNT(*) FROM element_food
UNION ALL
SELECT 'personnel', COUNT(*) FROM personnel
UNION ALL
SELECT 'management_personnel', COUNT(*) FROM management_personnel
UNION ALL
SELECT 'surveillance_personnel', COUNT(*) FROM surveillance_personnel
UNION ALL
SELECT 'research_personnel', COUNT(*) FROM research_personnel
UNION ALL
SELECT 'conservation_personnel', COUNT(*) FROM conservation_personnel
UNION ALL
SELECT 'research_projects', COUNT(*) FROM research_projects
UNION ALL
SELECT 'accommodations', COUNT(*) FROM accommodations
UNION ALL
SELECT 'visitors', COUNT(*) FROM visitors
UNION ALL
SELECT 'excursions', COUNT(*) FROM excursions
UNION ALL
SELECT 'accommodation_excursions', COUNT(*) FROM accommodation_excursions
UNION ALL
SELECT 'visitor_excursions', COUNT(*) FROM visitor_excursions
ORDER BY 
    `Row Count` DESC
INTO OUTFILE './results/table_row_counts.txt';

-- Get column information for each table
SELECT 
    TABLE_NAME as 'Table',
    COLUMN_NAME as 'Column',
    COLUMN_TYPE as 'Type',
    IS_NULLABLE as 'Nullable',
    COLUMN_KEY as 'Key',
    COLUMN_DEFAULT as 'Default',
    EXTRA as 'Extra'
FROM 
    information_schema.COLUMNS
WHERE 
    TABLE_SCHEMA = 'park_management'
ORDER BY 
    TABLE_NAME, ORDINAL_POSITION
INTO OUTFILE './results/table_columns.txt';
