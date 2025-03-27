import unittest
import pymysql

class TestExcursionsDataRequirements(unittest.TestCase):
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
            cursor.execute("DELETE FROM excursions WHERE day_of_week LIKE 'TEST%';")
        cls.connection.commit()
        cls.connection.close()

    def test_excursions_table_exists(self):
        """Test that the excursions table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'excursions';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Excursions table does not exist")

    def test_excursions_has_required_columns(self):
        """Test that excursions table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM excursions LIKE 'day_of_week';")
        day_of_week_column = self.cursor.fetchone()
        self.assertIsNotNone(day_of_week_column, "Excursions table does not have 'day_of_week' column")

        self.cursor.execute("SHOW COLUMNS FROM excursions LIKE 'time';")
        time_column = self.cursor.fetchone()
        self.assertIsNotNone(time_column, "Excursions table does not have 'time' column")

        self.cursor.execute("SHOW COLUMNS FROM excursions LIKE 'type';")
        type_column = self.cursor.fetchone()
        self.assertIsNotNone(type_column, "Excursions table does not have 'type' column")

    def test_excursions_data_insertion(self):
        """Test data insertion into excursions table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO excursions (day_of_week, time, type) VALUES ('TEST Sunday', '10:00:00', 'foot')")
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM excursions WHERE day_of_week = 'TEST Sunday'")
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into excursions table")

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into excursions table: {e}")

        finally:
            # Clean up test data
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM excursions WHERE day_of_week LIKE 'TEST%';")
            self.connection.commit()

    def test_excursions_required_fields_not_null(self):
        """Test that required fields (day_of_week, time, type) cannot be null"""
        try:
            # Try inserting data with NULL day_of_week
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO excursions (day_of_week, time, type) VALUES (NULL, '10:00:00', 'foot')")
                self.connection.commit()
            self.connection.rollback()

            # Try inserting data with NULL time
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO excursions (day_of_week, time, type) VALUES ('Test Day', NULL, 'foot')")
                self.connection.commit()
            self.connection.rollback()

            # Try inserting data with NULL type
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO excursions (day_of_week, time, type) VALUES ('Test Day', '10:00:00', NULL)")
                self.connection.commit()
            self.connection.rollback()

        finally:
            # Clean up the test data
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM excursions WHERE day_of_week LIKE 'TEST%';")
            self.connection.commit()

    def test_excursions_type_enum_values(self):
        """Test that the 'type' column only accepts ENUM values ('foot', 'vehicle')"""
        try:
            # Try inserting data with invalid type value
            with self.assertRaises(pymysql.err.DataError):
                self.cursor.execute("INSERT INTO excursions (day_of_week, time, type) VALUES ('Test Day', '10:00:00', 'invalid')")
                self.connection.commit()
            self.connection.rollback()

        finally:
            # Clean up the test data
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM excursions WHERE day_of_week LIKE 'TEST%';")
            self.connection.commit()
