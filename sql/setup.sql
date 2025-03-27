-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS park_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the created database
USE park_management;

-- Create tables (copied and adapted from test_database_connection.py)
CREATE TABLE IF NOT EXISTS provinces (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    responsible_organization VARCHAR(255) NOT NULL -- Made NOT NULL based on test_provinces.py
);

CREATE TABLE IF NOT EXISTS parks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    declaration_date DATE NOT NULL,
    contact_email VARCHAR(255),
    code VARCHAR(10) UNIQUE NOT NULL,
    total_area DECIMAL(15,2)
);

CREATE TABLE IF NOT EXISTS park_provinces (
    park_id INT,
    province_id INT,
    extension_in_province DECIMAL(15,2),
    FOREIGN KEY (park_id) REFERENCES parks(id) ON DELETE CASCADE, -- Added ON DELETE CASCADE
    FOREIGN KEY (province_id) REFERENCES provinces(id) ON DELETE CASCADE, -- Added ON DELETE CASCADE
    PRIMARY KEY (park_id, province_id)
);

CREATE TABLE IF NOT EXISTS park_areas (
    park_id INT,
    area_number INT,
    name VARCHAR(255),
    extension DECIMAL(15,2),
    PRIMARY KEY (park_id, area_number),
    FOREIGN KEY (park_id) REFERENCES parks(id) ON DELETE CASCADE -- Added ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS natural_elements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scientific_name VARCHAR(255) UNIQUE, -- Added UNIQUE constraint
    common_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS area_elements (
    park_id INT,
    area_number INT,
    element_id INT,
    number_of_individuals INT,
    PRIMARY KEY (park_id, area_number, element_id),
    FOREIGN KEY (park_id, area_number) REFERENCES park_areas(park_id, area_number) ON DELETE CASCADE, -- Added ON DELETE CASCADE
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) ON DELETE CASCADE -- Added ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vegetal_elements (
    element_id INT PRIMARY KEY,
    flowering_period VARCHAR(255),
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) ON DELETE CASCADE -- Added ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS animal_elements (
    element_id INT PRIMARY KEY,
    diet VARCHAR(255),
    mating_season VARCHAR(255),
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) ON DELETE CASCADE -- Added ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mineral_elements (
    element_id INT PRIMARY KEY,
    crystal_or_rock VARCHAR(255),
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) ON DELETE CASCADE -- Added ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS element_food (
    element_id INT,
    food_element_id INT,
    PRIMARY KEY (element_id, food_element_id),
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) ON DELETE CASCADE, -- Added ON DELETE CASCADE
    FOREIGN KEY (food_element_id) REFERENCES natural_elements(id) ON DELETE CASCADE -- Added ON DELETE CASCADE
    -- Removed CHECK constraints (check_mineral_not_food, check_vegetal_not_feeding)
    -- due to MySQL limitations on subqueries within CHECK.
    -- This logic needs to be enforced at the application level or via triggers.
);

CREATE TABLE IF NOT EXISTS personnel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    DNI VARCHAR(20) NOT NULL UNIQUE,
    CUIL VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    phone_numbers VARCHAR(255),
    salary DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS management_personnel (
    personnel_id INT PRIMARY KEY,
    entrance_number INT,
    FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE -- Added ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS surveillance_personnel (
    personnel_id INT PRIMARY KEY,
    vehicle_type VARCHAR(255),
    vehicle_registration VARCHAR(20),
    FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE -- Added ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS research_projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    budget DECIMAL(15,2) NOT NULL,
    duration VARCHAR(255) NOT NULL,
    element_id INT NOT NULL,
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) -- No cascade delete here, maybe project remains if element deleted? Or handle differently.
);

CREATE TABLE IF NOT EXISTS research_personnel (
    personnel_id INT, -- Changed to allow multiple personnel per project
    project_id INT,
    title VARCHAR(255), -- Titulation of the personnel for this project
    PRIMARY KEY (personnel_id, project_id), -- Composite key
    FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE, -- Added ON DELETE CASCADE
    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE -- Added ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS conservation_personnel (
    personnel_id INT PRIMARY KEY,
    specialty VARCHAR(255),
    park_id INT NOT NULL,
    area_number INT NOT NULL,
    FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE, -- Added ON DELETE CASCADE
    FOREIGN KEY (park_id, area_number) REFERENCES park_areas(park_id, area_number) ON DELETE CASCADE -- Added ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS accommodations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    capacity INT NOT NULL,
    category VARCHAR(255) UNIQUE -- Added UNIQUE constraint based on test setup
);

CREATE TABLE IF NOT EXISTS visitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    DNI VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    profession VARCHAR(255),
    accommodation_id INT,
    park_id INT, -- Added based on previous discussion for Func Req 3 testability
    FOREIGN KEY (accommodation_id) REFERENCES accommodations(id) ON DELETE SET NULL, -- Allow visitor if accommodation removed? Or CASCADE? SET NULL chosen.
    FOREIGN KEY (park_id) REFERENCES parks(id) ON DELETE CASCADE -- Added ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS excursions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    day_of_week VARCHAR(20) NOT NULL,
    time TIME NOT NULL,
    type ENUM('foot', 'vehicle') NOT NULL
);

CREATE TABLE IF NOT EXISTS accommodation_excursions (
    accommodation_id INT,
    excursion_id INT,
    PRIMARY KEY (accommodation_id, excursion_id),
    FOREIGN KEY (accommodation_id) REFERENCES accommodations(id) ON DELETE CASCADE, -- Added ON DELETE CASCADE
    FOREIGN KEY (excursion_id) REFERENCES excursions(id) ON DELETE CASCADE -- Added ON DELETE CASCADE
);

-- Table for Trigger Testing (Func Req 4)
CREATE TABLE IF NOT EXISTS email_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    park_email VARCHAR(255),
    element_scientific_name VARCHAR(255),
    old_count INT,
    new_count INT,
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger Implementation (Func Req 4 - Logging version)
DELIMITER //
CREATE TRIGGER species_decrease_email
AFTER UPDATE ON area_elements
FOR EACH ROW
BEGIN
    DECLARE park_contact_email VARCHAR(255);
    DECLARE element_name VARCHAR(255);

    -- Check if the number of individuals decreased
    IF NEW.number_of_individuals < OLD.number_of_individuals THEN
        -- Get the park's contact email
        SELECT contact_email INTO park_contact_email
        FROM parks
        WHERE id = NEW.park_id;

        -- Get the element's scientific name
        SELECT scientific_name INTO element_name
        FROM natural_elements
        WHERE id = NEW.element_id;

        -- Log the event instead of sending an email
        INSERT INTO email_log (park_email, element_scientific_name, old_count, new_count)
        VALUES (park_contact_email, element_name, OLD.number_of_individuals, NEW.number_of_individuals);
    END IF;
END;
//
DELIMITER ;

-- Stored Procedure (Additional Req 6 - Skeleton)
DELIMITER //
CREATE PROCEDURE compare_databases (IN db1_name VARCHAR(64), IN db2_name VARCHAR(64))
BEGIN
    -- Placeholder for comparison logic
    -- This will compare tables, indexes, constraints between db1_name and db2_name
    -- using INFORMATION_SCHEMA.
    SELECT 'Procedure compare_databases called with:', db1_name, db2_name;

    -- Example: Compare tables
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = db1_name
    AND table_name NOT IN (SELECT table_name FROM information_schema.tables WHERE table_schema = db2_name);

    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = db2_name
    AND table_name NOT IN (SELECT table_name FROM information_schema.tables WHERE table_schema = db1_name);

    -- Add more comparisons for columns, indexes, constraints etc.

END;
//
DELIMITER ;
