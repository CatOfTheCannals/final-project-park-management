import unittest
from unittest import TestCase
import pymysql

class TestDatabaseConnection(TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize database connection
        cls.connection = pymysql.connect(
            host='localhost',
            user='root', 
            password='',
            db='park_management'
        )
        
        # Create test tables if they don't exist
        with cls.connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS provinces (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    responsible_organization VARCHAR(255)
                );
                
                CREATE TABLE IF NOT EXISTS parks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    declaration_date DATE NOT NULL,
                    contact_email VARCHAR(255),
                    total_area DECIMAL(15,2)
                );

                CREATE TABLE IF NOT EXISTS park_provinces (
                    park_id INT,
                    province_id INT,
                    extension_in_province DECIMAL(15,2),
                    FOREIGN KEY (park_id) REFERENCES parks(id),
                    FOREIGN KEY (province_id) REFERENCES provinces(id),
                    PRIMARY KEY (park_id, province_id)
                );

                CREATE TABLE IF NOT EXISTS park_areas (
                    park_id INT,
                    area_number INT,
                    name VARCHAR(255),
                    extension DECIMAL(15,2),
                    PRIMARY KEY (park_id, area_number),
                    FOREIGN KEY (park_id) REFERENCES parks(id)
                );

                CREATE TABLE IF NOT EXISTS natural_elements (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    scientific_name VARCHAR(255),
                    common_name VARCHAR(255)
                );

                CREATE TABLE IF NOT EXISTS area_elements (
                    park_id INT,
                    area_number INT,
                    element_id INT,
                    number_of_individuals INT,
                    PRIMARY KEY (park_id, area_number, element_id),
                    FOREIGN KEY (park_id, area_number) REFERENCES park_areas(park_id, area_number),
                    FOREIGN KEY (element_id) REFERENCES natural_elements(id)
                );

                CREATE TABLE IF NOT EXISTS vegetal_elements (
                    element_id INT PRIMARY KEY,
                    flowering_period VARCHAR(255),
                    FOREIGN KEY (element_id) REFERENCES natural_elements(id)
                );

                CREATE TABLE IF NOT EXISTS animal_elements (
                    element_id INT PRIMARY KEY,
                    diet VARCHAR(255),
                    mating_season VARCHAR(255),
                    FOREIGN KEY (element_id) REFERENCES natural_elements(id)
                );

                CREATE TABLE IF NOT EXISTS mineral_elements (
                    element_id INT PRIMARY KEY,
                    crystal_or_rock VARCHAR(255),
                    FOREIGN KEY (element_id) REFERENCES natural_elements(id)
                );

                CREATE TABLE IF NOT EXISTS element_food (
                    element_id INT,
                    food_element_id INT,
                    PRIMARY KEY (element_id, food_element_id),
                    FOREIGN KEY (element_id) REFERENCES natural_elements(id),
                    FOREIGN KEY (food_element_id) REFERENCES natural_elements(id),
                    CONSTRAINT check_mineral_not_food CHECK (NOT EXISTS (
                        SELECT 1 FROM mineral_elements WHERE element_id = food_element_id
                    )),
                    CONSTRAINT check_vegetal_not_feeding CHECK (NOT EXISTS (
                        SELECT 1 FROM vegetal_elements WHERE element_id = element_id
                    ))
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
                    FOREIGN KEY (personnel_id) REFERENCES personnel(id)
                );

                CREATE TABLE IF NOT EXISTS surveillance_personnel (
                    personnel_id INT PRIMARY KEY,
                    vehicle_type VARCHAR(255),
                    vehicle_registration VARCHAR(20),
                    FOREIGN KEY (personnel_id) REFERENCES personnel(id)
                );

                CREATE TABLE IF NOT EXISTS research_projects (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    budget DECIMAL(15,2),
                    duration VARCHAR(255)
                );

                CREATE TABLE IF NOT EXISTS research_personnel (
                    personnel_id INT PRIMARY KEY,
                    title VARCHAR(255),
                    project_id INT,
                    FOREIGN KEY (personnel_id) REFERENCES personnel(id),
                    FOREIGN KEY (project_id) REFERENCES research_projects(id)
                );

                CREATE TABLE IF NOT EXISTS conservation_personnel (
                    personnel_id INT PRIMARY KEY,
                    specialty VARCHAR(255),
                    FOREIGN KEY (personnel_id) REFERENCES personnel(id)
                );

                CREATE TABLE IF NOT EXISTS accommodations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    capacity INT NOT NULL,
                    category VARCHAR(255)
                );

                CREATE TABLE IF NOT EXISTS visitors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    DNI VARCHAR(20) NOT NULL UNIQUE,
                    name VARCHAR(255) NOT NULL,
                    address VARCHAR(255),
                    profession VARCHAR(255),
                    accommodation_id INT,
                    FOREIGN KEY (accommodation_id) REFERENCES accommodations(id)
                );

                CREATE TABLE IF NOT EXISTS excursions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    day_of_week VARCHAR(20) NOT NULL,
                    time TIME NOT NULL,
                    type ENUM('foot', 'vehicle') NOT NULL
                );
            ''')
        cls.connection.commit()

    @classmethod
    def tearDownClass(cls):
        # Clean up test tables and close connection
        with cls.connection.cursor() as cursor:
            cursor.execute('''
                DROP TABLE IF EXISTS provinces;
                DROP TABLE IF EXISTS parks;
                DROP TABLE IF EXISTS park_provinces;
                DROP TABLE IF EXISTS park_areas;
                DROP TABLE IF EXISTS area_elements;
                DROP TABLE IF EXISTS natural_elements;
                DROP TABLE IF EXISTS vegetal_elements;
                DROP TABLE IF EXISTS animal_elements;
                DROP TABLE IF EXISTS mineral_elements;
                DROP TABLE IF EXISTS element_food;
                DROP TABLE IF EXISTS management_personnel;
                DROP TABLE IF EXISTS surveillance_personnel;
                DROP TABLE IF EXISTS research_personnel;
                DROP TABLE IF EXISTS research_projects;
                DROP TABLE IF EXISTS conservation_personnel;
                DROP TABLE IF EXISTS accommodations;
                DROP TABLE IF EXISTS visitors;
                DROP TABLE IF EXISTS excursions;
                DROP TABLE IF EXISTS personnel;
            ''')
        cls.connection.close()

    def test_01_connection_is_established(self):
        """Test that we can establish a database connection"""
        self.assertIsNotNone(TestDatabaseConnection.connection)
        
    def test_02_tables_are_created(self):
        """Test that required tables are created"""
        with TestDatabaseConnection.connection.cursor() as cursor:
            # Check provinces table exists
            cursor.execute("SHOW TABLES LIKE 'provinces';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'provinces')
            
            # Check parks table exists 
            cursor.execute("SHOW TABLES LIKE 'parks';") 
            result = cursor.fetchone()
            self.assertEqual(result[0], 'parks')

            # Check park_provinces table exists
            cursor.execute("SHOW TABLES LIKE 'park_provinces';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'park_provinces')

            # Check park_areas table exists
            cursor.execute("SHOW TABLES LIKE 'park_areas';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'park_areas')

            # Check natural_elements table exists
            cursor.execute("SHOW TABLES LIKE 'natural_elements';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'natural_elements')

            # Check area_elements table exists
            cursor.execute("SHOW TABLES LIKE 'area_elements';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'area_elements')

            # Check vegetal_elements table exists
            cursor.execute("SHOW TABLES LIKE 'vegetal_elements';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'vegetal_elements')

            # Check animal_elements table exists
            cursor.execute("SHOW TABLES LIKE 'animal_elements';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'animal_elements')

            # Check mineral_elements table exists
            cursor.execute("SHOW TABLES LIKE 'mineral_elements';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'mineral_elements')

            # Check element_food table exists
            cursor.execute("SHOW TABLES LIKE 'element_food';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'element_food')

            # Check personnel table exists
            cursor.execute("SHOW TABLES LIKE 'personnel';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'personnel')

            # Check management_personnel table exists
            cursor.execute("SHOW TABLES LIKE 'management_personnel';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'management_personnel')

            # Check surveillance_personnel table exists
            cursor.execute("SHOW TABLES LIKE 'surveillance_personnel';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'surveillance_personnel')

            # Check research_projects table exists
            cursor.execute("SHOW TABLES LIKE 'research_projects';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'research_projects')

            # Check research_personnel table exists
            cursor.execute("SHOW TABLES LIKE 'research_personnel';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'research_personnel')

            # Check conservation_personnel table exists
            cursor.execute("SHOW TABLES LIKE 'conservation_personnel';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'conservation_personnel')

            # Check accommodations table exists
            cursor.execute("SHOW TABLES LIKE 'accommodations';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'accommodations')

            # Check visitors table exists
            cursor.execute("SHOW TABLES LIKE 'visitors';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'visitors')

            # Check excursions table exists
            cursor.execute("SHOW TABLES LIKE 'excursions';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'excursions')
