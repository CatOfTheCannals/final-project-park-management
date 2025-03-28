from unittest import TestCase
import pymysql


class TestNaturalElementsDataRequirements(TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse the connection from previous tests
        cls.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='park_management'
        )
        cls.cursor = cls.connection.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def test_natural_elements_table_exists(self):
        """Test that the natural_elements table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'natural_elements';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Natural elements table does not exist")

    def test_natural_elements_has_required_columns(self):
        """Test that natural_elements table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM natural_elements LIKE 'scientific_name';")
        scientific_name_column = self.cursor.fetchone()
        self.assertIsNotNone(scientific_name_column, "Natural elements table does not have 'scientific_name' column")

        self.cursor.execute("SHOW COLUMNS FROM natural_elements LIKE 'common_name';")
        common_name_column = self.cursor.fetchone()
        self.assertIsNotNone(common_name_column, "Natural elements table does not have 'common_name' column")

# Removed TestAreaDataRequirements class - moved to test_area_elements.py
