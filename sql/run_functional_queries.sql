-- Script to run all functional requirement queries against the synthetic dataset
-- Outputs results to files for better analysis
USE park_management;

-- =============================================
-- FUNCTIONAL REQUIREMENT 1: Province with most parks
-- =============================================
SELECT '1. PROVINCE WITH MOST PARKS' AS 'Query'
INTO OUTFILE '/tmp/query1_header.txt';

SELECT p.name, COUNT(pp.park_id) AS park_count
FROM provinces p
JOIN park_provinces pp ON p.id = pp.province_id
GROUP BY p.id, p.name
ORDER BY park_count DESC
LIMIT 5
INTO OUTFILE '/tmp/query1_result.txt';

-- =============================================
-- FUNCTIONAL REQUIREMENT 2: Vegetal species in at least half of parks
-- =============================================
SELECT '2. VEGETAL SPECIES IN AT LEAST HALF OF PARKS' AS 'Query'
INTO OUTFILE '/tmp/query2_header.txt';

SELECT ne.scientific_name, COUNT(DISTINCT ae.park_id) as park_count, 
       (SELECT COUNT(*) FROM parks) as total_parks,
       (SELECT COUNT(*)/2 FROM parks) as half_parks_threshold
FROM natural_elements ne
JOIN vegetal_elements ve ON ne.id = ve.element_id
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING park_count >= (SELECT COUNT(*)/2 FROM parks)
ORDER BY park_count DESC
INTO OUTFILE '/tmp/query2_result.txt';

-- =============================================
-- FUNCTIONAL REQUIREMENT 3: Count visitors in parks with codes NH and IG
-- =============================================
SELECT '3. COUNT VISITORS IN PARKS WITH CODES NH AND IG' AS 'Query'
INTO OUTFILE '/tmp/query3_header.txt';

SELECT p.code, p.name, COUNT(v.id) as visitor_count
FROM visitors v
JOIN parks p ON v.park_id = p.id
WHERE p.code IN ('NH', 'IG')
GROUP BY p.code, p.name
INTO OUTFILE '/tmp/query3_result.txt';

-- Total count
SELECT COUNT(v.id) as total_visitor_count
FROM visitors v
JOIN parks p ON v.park_id = p.id
WHERE p.code IN ('NH', 'IG')
INTO OUTFILE '/tmp/query3_total.txt';

-- =============================================
-- ADDITIONAL REQUIREMENT 3: Species in all parks
-- =============================================
SELECT '4. SPECIES IN ALL PARKS' AS 'Query'
INTO OUTFILE '/tmp/query4_header.txt';

SELECT ne.scientific_name, COUNT(DISTINCT ae.park_id) as park_count, 
       (SELECT COUNT(*) FROM parks) as total_parks
FROM natural_elements ne
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING COUNT(DISTINCT ae.park_id) = (SELECT COUNT(*) FROM parks)
ORDER BY ne.scientific_name
INTO OUTFILE '/tmp/query4_result.txt';

-- =============================================
-- ADDITIONAL REQUIREMENT 4: Species in only one park
-- =============================================
SELECT '5. SPECIES IN ONLY ONE PARK' AS 'Query'
INTO OUTFILE '/tmp/query5_header.txt';

SELECT ne.scientific_name, 
       (SELECT p.name FROM parks p JOIN area_elements ae2 ON p.id = ae2.park_id 
        WHERE ae2.element_id = ne.id LIMIT 1) as park_name,
       COUNT(DISTINCT ae.park_id) as park_count
FROM natural_elements ne
JOIN area_elements ae ON ne.id = ae.element_id
GROUP BY ne.id, ne.scientific_name
HAVING COUNT(DISTINCT ae.park_id) = 1
ORDER BY ne.scientific_name
LIMIT 20
INTO OUTFILE '/tmp/query5_result.txt';

-- =============================================
-- TRIGGER TEST: Decrease species count to test email trigger
-- =============================================
SELECT '6. TRIGGER TEST: DECREASE SPECIES COUNT' AS 'Query'
INTO OUTFILE '/tmp/query6_header.txt';

-- Select a random area_element to update
SELECT ae.park_id, ae.area_number, ae.element_id, ae.number_of_individuals, 
       p.contact_email, ne.scientific_name
FROM area_elements ae
JOIN parks p ON ae.park_id = p.id
JOIN natural_elements ne ON ae.element_id = ne.id
WHERE ae.number_of_individuals > 10
LIMIT 1
INTO OUTFILE '/tmp/query6_candidate.txt';

-- Create a test script for the trigger
SELECT CONCAT(
    'UPDATE area_elements SET number_of_individuals = number_of_individuals - 5 ',
    'WHERE park_id = ', park_id, ' AND area_number = ', area_number, 
    ' AND element_id = ', element_id, ';'
) AS trigger_test_command
FROM area_elements
WHERE number_of_individuals > 10
LIMIT 1
INTO OUTFILE '/tmp/trigger_test_command.sql';

-- Create a script to check the email_log table
SELECT 'SELECT * FROM email_log ORDER BY log_timestamp DESC LIMIT 5;' AS check_email_log
INTO OUTFILE '/tmp/check_email_log.sql';
