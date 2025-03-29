-- Script to analyze execution plans for the functional requirement queries
USE park_management;

-- =============================================
-- FUNCTIONAL REQUIREMENT 1: Province with most parks
-- =============================================
SELECT 'EXECUTION PLAN FOR FUNCTIONAL REQUIREMENT 1: Province with most parks' AS 'Analysis';

-- Before adding index
EXPLAIN FORMAT=JSON
SELECT p.name, COUNT(pp.park_id) AS park_count
FROM provinces p
JOIN park_provinces pp ON p.id = pp.province_id
GROUP BY p.id, p.name
ORDER BY park_count DESC
LIMIT 1;

-- Create index if it doesn't exist
-- Note: This is likely redundant as InnoDB automatically creates indexes for foreign keys
CREATE INDEX IF NOT EXISTS idx_park_provinces_province_id ON park_provinces(province_id);

-- After adding index
EXPLAIN FORMAT=JSON
SELECT p.name, COUNT(pp.park_id) AS park_count
FROM provinces p
JOIN park_provinces pp ON p.id = pp.province_id
GROUP BY p.id, p.name
ORDER BY park_count DESC
LIMIT 1;

-- Actual query result
SELECT p.name, COUNT(pp.park_id) AS park_count
FROM provinces p
JOIN park_provinces pp ON p.id = pp.province_id
GROUP BY p.id, p.name
ORDER BY park_count DESC
LIMIT 1;

-- =============================================
-- FUNCTIONAL REQUIREMENT 2: Vegetal species in at least half of parks
-- =============================================
SELECT 'EXECUTION PLAN FOR FUNCTIONAL REQUIREMENT 2: Vegetal species in at least half of parks' AS 'Analysis';

-- Before adding index
EXPLAIN FORMAT=JSON
SELECT ne.scientific_name, COUNT(DISTINCT ae.park_id) as park_count
FROM natural_elements ne
JOIN vegetal_elements ve ON ne.id = ve.element_id
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING park_count >= (SELECT COUNT(*)/2 FROM parks);

-- Create indexes if they don't exist
CREATE INDEX IF NOT EXISTS idx_area_elements_element_id ON area_elements(element_id);
CREATE INDEX IF NOT EXISTS idx_area_elements_park_id ON area_elements(park_id);
CREATE INDEX IF NOT EXISTS idx_natural_elements_scientific_name ON natural_elements(scientific_name);

-- After adding indexes
EXPLAIN FORMAT=JSON
SELECT ne.scientific_name, COUNT(DISTINCT ae.park_id) as park_count
FROM natural_elements ne
JOIN vegetal_elements ve ON ne.id = ve.element_id
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING park_count >= (SELECT COUNT(*)/2 FROM parks);

-- Actual query result
SELECT ne.scientific_name, COUNT(DISTINCT ae.park_id) as park_count, 
       (SELECT COUNT(*)/2 FROM parks) as half_parks_count
FROM natural_elements ne
JOIN vegetal_elements ve ON ne.id = ve.element_id
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING park_count >= (SELECT COUNT(*)/2 FROM parks);

-- =============================================
-- FUNCTIONAL REQUIREMENT 3: Count visitors in parks with codes A and B
-- =============================================
SELECT 'EXECUTION PLAN FOR FUNCTIONAL REQUIREMENT 3: Count visitors in parks with codes A and B' AS 'Analysis';

-- Before adding index
EXPLAIN FORMAT=JSON
SELECT COUNT(v.id) as visitor_count
FROM visitors v
JOIN parks p ON v.park_id = p.id
WHERE p.code IN ('A', 'B');

-- Create index if it doesn't exist
CREATE INDEX IF NOT EXISTS idx_parks_code ON parks(code);
CREATE INDEX IF NOT EXISTS idx_visitors_park_id ON visitors(park_id);

-- After adding index
EXPLAIN FORMAT=JSON
SELECT COUNT(v.id) as visitor_count
FROM visitors v
JOIN parks p ON v.park_id = p.id
WHERE p.code IN ('A', 'B');

-- Actual query result
SELECT COUNT(v.id) as visitor_count
FROM visitors v
JOIN parks p ON v.park_id = p.id
WHERE p.code IN ('A', 'B');

-- =============================================
-- ADDITIONAL REQUIREMENT 3: Species in all parks
-- =============================================
SELECT 'EXECUTION PLAN FOR ADDITIONAL REQUIREMENT 3: Species in all parks' AS 'Analysis';

-- Before adding index (using existing indexes from previous queries)
EXPLAIN FORMAT=JSON
SELECT ne.scientific_name
FROM natural_elements ne
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING COUNT(DISTINCT ae.park_id) = (SELECT COUNT(*) FROM parks);

-- After adding indexes (already added in previous steps)
EXPLAIN FORMAT=JSON
SELECT ne.scientific_name
FROM natural_elements ne
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING COUNT(DISTINCT ae.park_id) = (SELECT COUNT(*) FROM parks);

-- Actual query result
SELECT ne.scientific_name, COUNT(DISTINCT ae.park_id) as park_count, 
       (SELECT COUNT(*) FROM parks) as total_parks
FROM natural_elements ne
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING COUNT(DISTINCT ae.park_id) = (SELECT COUNT(*) FROM parks);

-- =============================================
-- ADDITIONAL REQUIREMENT 4: Species in only one park
-- =============================================
SELECT 'EXECUTION PLAN FOR ADDITIONAL REQUIREMENT 4: Species in only one park' AS 'Analysis';

-- Using existing indexes
EXPLAIN FORMAT=JSON
SELECT ne.scientific_name
FROM natural_elements ne
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING COUNT(DISTINCT ae.park_id) = 1;

-- Actual query result
SELECT ne.scientific_name, COUNT(DISTINCT ae.park_id) as park_count
FROM natural_elements ne
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING COUNT(DISTINCT ae.park_id) = 1;

-- =============================================
-- Summary of indexes created
-- =============================================
SELECT 'SUMMARY OF INDEXES CREATED' AS 'Analysis';

SELECT 
    table_name, 
    index_name, 
    GROUP_CONCAT(column_name ORDER BY seq_in_index) AS indexed_columns,
    index_type,
    is_visible
FROM 
    information_schema.statistics
WHERE 
    table_schema = 'park_management'
GROUP BY 
    table_name, index_name, index_type, is_visible
ORDER BY 
    table_name, index_name;
