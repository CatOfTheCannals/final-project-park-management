-- Create an alternative database schema for comparison purposes
CREATE DATABASE IF NOT EXISTS park_management_alt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE park_management_alt;

-- Create tables similar to park_management, but with intentional differences

-- Provinces: Missing UNIQUE constraint on name
CREATE TABLE IF NOT EXISTS provinces (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL, -- Removed UNIQUE
    responsible_organization VARCHAR(255) NOT NULL
);

-- Parks: Missing index on code
CREATE TABLE IF NOT EXISTS parks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    declaration_date DATE NOT NULL,
    contact_email VARCHAR(255),
    code VARCHAR(10) UNIQUE NOT NULL, -- Keep UNIQUE constraint for FKs, but index will be missing
    total_area DECIMAL(15,2)
);
-- Deliberately omit CREATE INDEX idx_parks_code ON parks(code);

CREATE TABLE IF NOT EXISTS park_provinces (
    park_id INT,
    province_id INT,
    extension_in_province DECIMAL(15,2),
    FOREIGN KEY (park_id) REFERENCES parks(id) ON DELETE CASCADE,
    FOREIGN KEY (province_id) REFERENCES provinces(id) ON DELETE CASCADE,
    PRIMARY KEY (park_id, province_id)
);
-- Add index matching the main schema for fair comparison where tables exist
CREATE INDEX idx_park_provinces_province_id ON park_provinces(province_id);


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
    common_name VARCHAR(255) UNIQUE
);
-- Add index matching the main schema
CREATE INDEX idx_natural_elements_scientific_name ON natural_elements(scientific_name);


CREATE TABLE IF NOT EXISTS area_elements (
    park_id INT,
    area_number INT,
    element_id INT,
    number_of_individuals INT,
    PRIMARY KEY (park_id, area_number, element_id),
    FOREIGN KEY (park_id, area_number) REFERENCES park_areas(park_id, area_number) ON DELETE CASCADE,
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) ON DELETE CASCADE
);
-- Add indexes matching the main schema
CREATE INDEX idx_area_elements_element_id ON area_elements(element_id);
CREATE INDEX idx_area_elements_park_id ON area_elements(park_id);


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

-- Mineral Elements: Keep the same
CREATE TABLE IF NOT EXISTS mineral_elements (
    element_id INT PRIMARY KEY,
    crystal_or_rock VARCHAR(255),
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) ON DELETE CASCADE
);

-- Element Food: Keep the same (triggers omitted as they depend on other tables)
CREATE TABLE IF NOT EXISTS element_food (
    element_id INT,
    food_element_id INT,
    PRIMARY KEY (element_id, food_element_id),
    FOREIGN KEY (element_id) REFERENCES natural_elements(id) ON DELETE CASCADE,
    FOREIGN KEY (food_element_id) REFERENCES natural_elements(id) ON DELETE CASCADE
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
    title VARCHAR(255),
    PRIMARY KEY (personnel_id, project_id),
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

-- Visitors: Missing foreign key for park_id
CREATE TABLE IF NOT EXISTS visitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    DNI VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    profession VARCHAR(255),
    accommodation_id INT,
    park_id INT, -- Column exists but FK is missing
    FOREIGN KEY (accommodation_id) REFERENCES accommodations(id) ON DELETE SET NULL
    -- Deliberately omit FOREIGN KEY (park_id) REFERENCES parks(id) ON DELETE CASCADE
);
-- Add index matching the main schema
CREATE INDEX idx_visitors_park_id ON visitors(park_id);


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

-- Deliberately omit the email_log table and its trigger
-- Deliberately omit the compare_databases procedure

-- Additional tables for the alternative schema

-- Eco Innovations: Capturing sustainable projects and innovations in parks
CREATE TABLE IF NOT EXISTS eco_innovations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    park_id INT,
    innovation_name VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (park_id) REFERENCES parks(id) ON DELETE CASCADE
);

-- Adventure Trails: Recording exciting trail information for park visitors
CREATE TABLE IF NOT EXISTS adventure_trails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    park_id INT,
    trail_name VARCHAR(255) NOT NULL,
    length DECIMAL(10,2) NOT NULL,
    difficulty ENUM('Easy','Moderate','Hard') NOT NULL,
    FOREIGN KEY (park_id) REFERENCES parks(id) ON DELETE CASCADE
);


SELECT 'Alternative database schema created.' AS status;
