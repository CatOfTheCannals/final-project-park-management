import unittest
from unittest import TestCase
import pymysql


class TestMineralElementsDataRequirements(TestCase):
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

    def test_mineral_elements_table_exists(self):
        """Test that the mineral_elements table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'mineral_elements';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Mineral elements table does not exist")

    def test_mineral_elements_has_required_columns(self):
        """Test that mineral_elements table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM mineral_elements LIKE 'crystal_or_rock';")
        crystal_or_rock_column = self.cursor.fetchone()
        self.assertIsNotNone(crystal_or_rock_column, "Mineral elements table does not have 'crystal_or_rock' column")
