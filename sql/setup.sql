-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS park_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the created database
USE park_management;

-- Drop existing triggers to avoid errors on re-run
DROP TRIGGER IF EXISTS check_element_food_before_insert;
DROP TRIGGER IF EXISTS check_element_food_before_update;
DROP TRIGGER IF EXISTS species_decrease_email;

-- Create tables (copied and adapted from test_database_connection.py)
CREATE TABLE IF NOT EXISTS provinces (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    responsible_organization VARCHAR(255) NOT NULL
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
    FOREIGN KEY (park_id) REFERENCES parks(id) ON DELETE CASCADE, 
    FOREIGN KEY (province_id) REFERENCES provinces(id) ON DELETE CASCADE, 
    PRIMARY KEY (park_id, province_id)
);

CREATE TABLE IF NOT EXISTS park_areas (
    park_id INT,
    area_number INT,
    name VARCHAR(255),
    extension DECIMAL(15,2),
    PRIMARY KEY (park_id, area_number),
    FOREIGN KEY (park_id) REFERENCES parks(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS natural_elements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scientific_name VARCHAR(255) UNIQUE,
    common_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS area_elements (
    park_id INT,
    area_number INT,
    element_id INT,
    number_of_individuals INT,
    PRIMARY KEY (park_id, area_number, element_id),
    FOREIGN KEY (park_id, area_number) REFERENCES park_areas(park_id, area_number) ON DELETE CASCADE,
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vegetal_elements (
    element_id INT PRIMARY KEY,
    flowering_period VARCHAR(255),
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS animal_elements (
    element_id INT PRIMARY KEY,
    diet VARCHAR(255),
    mating_season VARCHAR(255),
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mineral_elements (
    element_id INT PRIMARY KEY,
    crystal_or_rock VARCHAR(255),
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS element_food (
    element_id INT,
    food_element_id INT,
    PRIMARY KEY (element_id, food_element_id),
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) ON DELETE CASCADE,
    FOREIGN KEY (food_element_id) REFERENCES natural_elements(id) ON DELETE CASCADE
);

-- Triggers to enforce element_food constraints (MySQL < 8.0.16 CHECK alternative)
DELIMITER //

CREATE TRIGGER check_element_food_before_insert
BEFORE INSERT ON element_food
FOR EACH ROW
BEGIN
    DECLARE is_mineral INT;
    DECLARE is_vegetal INT;

    -- Check if food_element_id is a mineral
    SELECT COUNT(*) INTO is_mineral
    FROM mineral_elements me
    WHERE me.element_id = NEW.food_element_id;

    IF is_mineral > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Constraint violation: Minerals cannot be food (element_food).';
    END IF;

    -- Check if element_id is a vegetal
    SELECT COUNT(*) INTO is_vegetal
    FROM vegetal_elements ve
    WHERE ve.element_id = NEW.element_id;

    IF is_vegetal > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Constraint violation: Vegetals cannot feed on other elements (element_food).';
    END IF;
END //

CREATE TRIGGER check_element_food_before_update
BEFORE UPDATE ON element_food
FOR EACH ROW
BEGIN
    DECLARE is_mineral INT;
    DECLARE is_vegetal INT;

    -- Check if food_element_id is a mineral
    SELECT COUNT(*) INTO is_mineral
    FROM mineral_elements me
    WHERE me.element_id = NEW.food_element_id;

    IF is_mineral > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Constraint violation: Minerals cannot be food (element_food).';
    END IF;

    -- Check if element_id is a vegetal
    SELECT COUNT(*) INTO is_vegetal
    FROM vegetal_elements ve
    WHERE ve.element_id = NEW.element_id;

    IF is_vegetal > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Constraint violation: Vegetals cannot feed on other elements (element_food).';
    END IF;
END //

DELIMITER ;


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
    FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS surveillance_personnel (
    personnel_id INT PRIMARY KEY,
    vehicle_type VARCHAR(255),
    vehicle_registration VARCHAR(20),
    FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS research_projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    budget DECIMAL(15,2) NOT NULL,
    duration VARCHAR(255) NOT NULL,
    element_id INT NOT NULL,
    FOREIGN KEY (element_id) REFERENCES natural_elements(id)
);

CREATE TABLE IF NOT EXISTS research_personnel (
    personnel_id INT, 
    project_id INT,
    title VARCHAR(255), -- Titulation of the personnel for this project
    PRIMARY KEY (personnel_id, project_id), -- Composite key
    FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS conservation_personnel (
    personnel_id INT PRIMARY KEY,
    specialty VARCHAR(255),
    park_id INT NOT NULL,
    area_number INT NOT NULL,
    FOREIGN KEY (personnel_id) REFERENCES personnel(id) ON DELETE CASCADE,
    FOREIGN KEY (park_id, area_number) REFERENCES park_areas(park_id, area_number) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS accommodations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    capacity INT NOT NULL,
    category VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS visitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    DNI VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    profession VARCHAR(255),
    accommodation_id INT,
    park_id INT, 
    FOREIGN KEY (accommodation_id) REFERENCES accommodations(id) ON DELETE SET NULL, 
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
    FOREIGN KEY (accommodation_id) REFERENCES accommodations(id) ON DELETE CASCADE,
    FOREIGN KEY (excursion_id) REFERENCES excursions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS visitor_excursions (
    visitor_id INT,
    excursion_id INT,
    PRIMARY KEY (visitor_id, excursion_id),
    FOREIGN KEY (visitor_id) REFERENCES visitors(id) ON DELETE CASCADE,
    FOREIGN KEY (excursion_id) REFERENCES excursions(id) ON DELETE CASCADE
);

-- Table for Trigger Testing
CREATE TABLE IF NOT EXISTS email_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    park_email VARCHAR(255),
    element_scientific_name VARCHAR(255),
    old_count INT,
    new_count INT,
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger Implementation (Logging version)
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
END //
DELIMITER ;
