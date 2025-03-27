import unittest
import pymysql

class TestAccommodationsDataRequirements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse the connection from previous tests
        cls.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='park_management',
            cursorclass=pymysql.cursors.DictCursor
        )
        cls.cursor = cls.connection.cursor()

    @classmethod
    def tearDownClass(cls):
        # Clean up test data
        with cls.connection.cursor() as cursor:
            cursor.execute("DELETE FROM accommodations WHERE category LIKE 'TEST%';")
        cls.connection.commit()
        cls.connection.close()

    def test_accommodations_table_exists(self):
        """Test that the accommodations table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'accommodations';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Accommodations table does not exist")

    def test_accommodations_has_required_columns(self):
        """Test that accommodations table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM accommodations LIKE 'capacity';")
        capacity_column = self.cursor.fetchone()
        self.assertIsNotNone(capacity_column, "Accommodations table does not have 'capacity' column")

        self.cursor.execute("SHOW COLUMNS FROM accommodations LIKE 'category';")
        category_column = self.cursor.fetchone()
        self.assertIsNotNone(category_column, "Accommodations table does not have 'category' column")

    def test_accommodations_data_insertion(self):
        """Test data insertion into accommodations table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO accommodations (capacity, category) VALUES (4, 'TEST Cabin')")
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM accommodations WHERE category = 'TEST Cabin'")
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into accommodations table")

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into accommodations table: {e}")

        finally:
            # Clean up test data
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM accommodations WHERE category LIKE 'TEST%';")
            self.connection.commit()

    def test_accommodations_required_fields_not_null(self):
        """Test that required fields (capacity) cannot be null"""
        try:
            # Try inserting data with NULL capacity
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO accommodations (capacity, category) VALUES (NULL, 'Test Category')")
                self.connection.commit()
            self.connection.rollback()

        finally:
            # Clean up the test data
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM accommodations WHERE category LIKE 'TEST%';")
            self.connection.commit()
