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
                    name VARCHAR(255) NOT NULL UNIQUE
                );
                
                CREATE TABLE IF NOT EXISTS parks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    declaration_date DATE NOT NULL,
                    contact_email VARCHAR(255),
                    total_area DECIMAL(15,2)
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
