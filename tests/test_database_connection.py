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
