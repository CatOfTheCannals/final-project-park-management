from unittest import TestCase
import pymysql


class TestParksDataRequirements(TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse the connection from previous tests
        cls.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='park_management',
            cursorclass=pymysql.cursors.DictCursor # Use DictCursor for easier access to column names
        )
        cls.cursor = cls.connection.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def test_parks_table_exists(self):
        """Test that the parks table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'parks';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Parks table does not exist")

    def parks_has_required_columns(self):
        """Test that parks table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM parks LIKE 'name';")
        name_column = self.cursor.fetchone()
        self.assertIsNotNone(name_column, "Parks table does not have 'name' column")

        self.cursor.execute("SHOW COLUMNS FROM parks LIKE 'declaration_date';")
        date_column = self.cursor.fetchone()
        self.assertIsNotNone(date_column, "Parks table does not have 'declaration_date' column")

        self.cursor.execute("SHOW COLUMNS FROM parks LIKE 'contact_email';")
        email_column = self.cursor.fetchone()
        self.assertIsNotNone(email_column, "Parks table does not have 'contact_email' column")

        self.cursor.execute("SHOW COLUMNS FROM parks LIKE 'total_area';")
        area_column = self.cursor.fetchone()
        self.assertIsNotNone(area_column, "Parks table does not have 'total_area' column")

    def test_parks_has_code_column(self):
        """Test that parks table has code column"""
        self.cursor.execute("SHOW COLUMNS FROM parks LIKE 'code';")
        code_column = self.cursor.fetchone()
        self.assertIsNotNone(code_column, "Parks table does not have 'code' column")
