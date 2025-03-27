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
        # Connection is established here, assuming the database exists
        # Table creation is handled by sql/setup.sql

    @classmethod
    def tearDownClass(cls):
        # Close the connection
        # Table dropping is handled by sql/teardown.sql
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

            # Check accommodation_excursions table exists
            cursor.execute("SHOW TABLES LIKE 'accommodation_excursions';")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'accommodation_excursions')
