-- Populate park_management database using LOAD DATA LOCAL INFILE
-- Run this script AFTER running setup.sql
-- Ensure MySQL server and client are configured with 'local_infile=1'

USE park_management;

-- Disable foreign key checks for bulk loading
SET FOREIGN_KEY_CHECKS=0;

-- =============================================
-- LOAD DATA INTO TABLES
-- =============================================

-- provinces
LOAD DATA LOCAL INFILE 'data/load/provinces.csv'
INTO TABLE provinces
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS -- Skip header row
(id, name, responsible_organization);

-- parks
LOAD DATA LOCAL INFILE 'data/load/parks.csv'
INTO TABLE parks
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, name, declaration_date, contact_email, code, total_area);

-- park_provinces
LOAD DATA LOCAL INFILE 'data/load/park_provinces.csv'
INTO TABLE park_provinces
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(park_id, province_id, extension_in_province);

-- park_areas
LOAD DATA LOCAL INFILE 'data/load/park_areas.csv'
INTO TABLE park_areas
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(park_id, area_number, name, extension);

-- natural_elements
LOAD DATA LOCAL INFILE 'data/load/natural_elements.csv'
INTO TABLE natural_elements
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, scientific_name, common_name);

-- animal_elements
LOAD DATA LOCAL INFILE 'data/load/animal_elements.csv'
INTO TABLE animal_elements
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(element_id, diet, mating_season);

-- vegetal_elements
LOAD DATA LOCAL INFILE 'data/load/vegetal_elements.csv'
INTO TABLE vegetal_elements
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(element_id, flowering_period);

-- mineral_elements
LOAD DATA LOCAL INFILE 'data/load/mineral_elements.csv'
INTO TABLE mineral_elements
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(element_id, crystal_or_rock);

-- area_elements
LOAD DATA LOCAL INFILE 'data/load/area_elements.csv'
INTO TABLE area_elements
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(park_id, area_number, element_id, number_of_individuals);

-- element_food
LOAD DATA LOCAL INFILE 'data/load/element_food.csv'
INTO TABLE element_food
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(element_id, food_element_id);

-- personnel
LOAD DATA LOCAL INFILE 'data/load/personnel.csv'
INTO TABLE personnel
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, DNI, CUIL, name, address, phone_numbers, salary);

-- research_projects
LOAD DATA LOCAL INFILE 'data/load/research_projects.csv'
INTO TABLE research_projects
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, budget, duration, element_id);

-- management_personnel
LOAD DATA LOCAL INFILE 'data/load/management_personnel.csv'
INTO TABLE management_personnel
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(personnel_id, entrance_number);

-- surveillance_personnel
LOAD DATA LOCAL INFILE 'data/load/surveillance_personnel.csv'
INTO TABLE surveillance_personnel
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(personnel_id, vehicle_type, vehicle_registration);

-- research_personnel
LOAD DATA LOCAL INFILE 'data/load/research_personnel.csv'
INTO TABLE research_personnel
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(personnel_id, project_id, title);

-- conservation_personnel
LOAD DATA LOCAL INFILE 'data/load/conservation_personnel.csv'
INTO TABLE conservation_personnel
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(personnel_id, specialty, park_id, area_number);

-- accommodations
LOAD DATA LOCAL INFILE 'data/load/accommodations.csv'
INTO TABLE accommodations
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, capacity, category);

-- excursions
LOAD DATA LOCAL INFILE 'data/load/excursions.csv'
INTO TABLE excursions
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, day_of_week, time, type);

-- accommodation_excursions
LOAD DATA LOCAL INFILE 'data/load/accommodation_excursions.csv'
INTO TABLE accommodation_excursions
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(accommodation_id, excursion_id);

-- visitors
LOAD DATA LOCAL INFILE 'data/load/visitors.csv'
INTO TABLE visitors
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, DNI, name, address, profession, accommodation_id, park_id);

-- visitor_excursions
LOAD DATA LOCAL INFILE 'data/load/visitor_excursions.csv'
INTO TABLE visitor_excursions
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(visitor_id, excursion_id);

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS=1;

-- Clean up temporary function if it exists from previous INSERT version
DROP FUNCTION IF EXISTS random_individuals;

-- Verify data population (Optional: Can be commented out for production use)
SELECT 'Data population from CSV complete.' AS status;
SELECT COUNT(*) AS provinces_count FROM provinces;
SELECT COUNT(*) AS parks_count FROM parks;
SELECT COUNT(*) AS park_provinces_count FROM park_provinces;
SELECT COUNT(*) AS park_areas_count FROM park_areas;
SELECT COUNT(*) AS natural_elements_count FROM natural_elements;
SELECT COUNT(*) AS animal_elements_count FROM animal_elements;
SELECT COUNT(*) AS vegetal_elements_count FROM vegetal_elements;
SELECT COUNT(*) AS mineral_elements_count FROM mineral_elements;
SELECT COUNT(*) AS area_elements_count FROM area_elements;
SELECT COUNT(*) AS element_food_count FROM element_food;
SELECT COUNT(*) AS personnel_count FROM personnel;
SELECT COUNT(*) AS research_projects_count FROM research_projects;
SELECT COUNT(*) AS accommodations_count FROM accommodations;
SELECT COUNT(*) AS visitors_count FROM visitors;
SELECT COUNT(*) AS excursions_count FROM excursions;
SELECT COUNT(*) AS accommodation_excursions_count FROM accommodation_excursions;
SELECT COUNT(*) AS visitor_excursions_count FROM visitor_excursions;