-- Script to run all functional requirement queries against the synthetic dataset
USE park_management;

-- =============================================
-- FUNCTIONAL REQUIREMENT 1: Province with most parks
-- =============================================
SELECT '1. PROVINCE WITH MOST PARKS' AS 'Query';

SELECT p.name, COUNT(pp.park_id) AS park_count
FROM provinces p
JOIN park_provinces pp ON p.id = pp.province_id
GROUP BY p.id, p.name
ORDER BY park_count DESC
LIMIT 5;

-- =============================================
-- FUNCTIONAL REQUIREMENT 2: Vegetal species in at least half of parks
-- =============================================
SELECT '2. VEGETAL SPECIES IN AT LEAST HALF OF PARKS' AS 'Query';

SELECT ne.scientific_name, COUNT(DISTINCT ae.park_id) as park_count, 
       (SELECT COUNT(*) FROM parks) as total_parks,
       (SELECT COUNT(*)/2 FROM parks) as half_parks_threshold
FROM natural_elements ne
JOIN vegetal_elements ve ON ne.id = ve.element_id
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING park_count >= (SELECT COUNT(*)/2 FROM parks)
ORDER BY park_count DESC;

-- =============================================
-- FUNCTIONAL REQUIREMENT 3: Count visitors in parks with codes A and B
-- =============================================
SELECT '3. COUNT VISITORS IN PARKS WITH CODES A AND B' AS 'Query';

SELECT p.code, p.name, COUNT(v.id) as visitor_count
FROM visitors v
JOIN parks p ON v.park_id = p.id
WHERE p.code IN ('A', 'B')
GROUP BY p.code, p.name;

-- Total count
SELECT COUNT(v.id) as total_visitor_count
FROM visitors v
JOIN parks p ON v.park_id = p.id
WHERE p.code IN ('A', 'B');

-- =============================================
-- ADDITIONAL REQUIREMENT 3: Species in all parks
-- =============================================
SELECT '4. SPECIES IN ALL PARKS' AS 'Query';

SELECT ne.scientific_name, COUNT(DISTINCT ae.park_id) as park_count, 
       (SELECT COUNT(*) FROM parks) as total_parks
FROM natural_elements ne
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING COUNT(DISTINCT ae.park_id) = (SELECT COUNT(*) FROM parks)
ORDER BY ne.scientific_name;

-- =============================================
-- ADDITIONAL REQUIREMENT 4: Species in only one park
-- =============================================
SELECT '5. SPECIES IN ONLY ONE PARK' AS 'Query';

SELECT ne.scientific_name, 
       (SELECT p.name FROM parks p JOIN area_elements ae2 ON p.id = ae2.park_id 
        WHERE ae2.element_id = ne.id LIMIT 1) as park_name,
       COUNT(DISTINCT ae.park_id) as park_count
FROM natural_elements ne
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING COUNT(DISTINCT ae.park_id) = 1
ORDER BY ne.scientific_name
LIMIT 20;  -- Limit to 20 results as there might be many

-- =============================================
-- TRIGGER TEST: Decrease species count to test email trigger
-- =============================================
SELECT '6. TRIGGER TEST: DECREASE SPECIES COUNT' AS 'Query';

-- Select a random area_element to update
SELECT ae.park_id, ae.area_number, ae.element_id, ae.number_of_individuals, 
       p.contact_email, ne.scientific_name
FROM area_elements ae
JOIN parks p ON ae.park_id = p.id
JOIN natural_elements ne ON ae.element_id = ne.id
WHERE ae.number_of_individuals > 10
LIMIT 1;

-- Note: To test the trigger, you would run an UPDATE statement like:
-- UPDATE area_elements 
-- SET number_of_individuals = number_of_individuals - 5
-- WHERE park_id = X AND area_number = Y AND element_id = Z;

-- Then check the email_log table:
-- SELECT * FROM email_log ORDER BY log_timestamp DESC LIMIT 5;
