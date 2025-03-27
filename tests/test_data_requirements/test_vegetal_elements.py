from unittest import TestCase
import pymysql


class TestVegetalElementsDataRequirements(TestCase):
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

    def test_vegetal_elements_table_exists(self):
        """Test that the vegetal_elements table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'vegetal_elements';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Vegetal elements table does not exist")

    def test_vegetal_elements_has_required_columns(self):
        """Test that vegetal_elements table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM vegetal_elements LIKE 'flowering_period';")
        flowering_period_column = self.cursor.fetchone()
        self.assertIsNotNone(flowering_period_column, "Vegetal elements table does not have 'flowering_period' column")
