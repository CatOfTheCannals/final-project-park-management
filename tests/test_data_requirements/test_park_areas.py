from unittest import TestCase
import pymysql


class TestParkAreasDataRequirements(TestCase):
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

    def park_areas_table_exists(self):
        """Test that the park_areas table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'park_areas';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Park areas table does not exist")

    def park_areas_has_required_columns(self):
        """Test that park_areas table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM park_areas LIKE 'name';")
        name_column = self.cursor.fetchone()
        self.assertIsNotNone(name_column, "Park areas table does not have 'name' column")

        self.cursor.execute("SHOW COLUMNS FROM park_areas LIKE 'extension';")
        extension_column = self.cursor.fetchone()
        self.assertIsNotNone(extension_column, "Park areas table does not have 'extension' column")
