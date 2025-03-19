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
