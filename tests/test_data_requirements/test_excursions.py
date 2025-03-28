import unittest
import pymysql

class TestExcursionsDataRequirements(unittest.TestCase):
    # Use setUp and tearDown for test isolation
    def setUp(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='park_management',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()
        self.created_ids = [] # Track created IDs

    def tearDown(self):
        # Clean up test data created during tests
        if self.created_ids:
            with self.connection.cursor() as cursor:
                ids_format = ','.join(['%s'] * len(self.created_ids))
                # Need to delete from linking tables first if any test creates links
                cursor.execute(f"DELETE FROM accommodation_excursions WHERE excursion_id IN ({ids_format})", tuple(self.created_ids))
                cursor.execute(f"DELETE FROM visitor_excursions WHERE excursion_id IN ({ids_format})", tuple(self.created_ids))
                cursor.execute(f"DELETE FROM excursions WHERE id IN ({ids_format})", tuple(self.created_ids))
            self.connection.commit()
        self.connection.close()

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
            # Insert valid data
            self.cursor.execute("INSERT INTO excursions (day_of_week, time, type) VALUES ('TEST_E_Sunday', '10:00:00', 'foot')")
            inserted_id = self.cursor.lastrowid
            self.created_ids.append(inserted_id) # Track ID
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM excursions WHERE id = %s", (inserted_id,))
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into excursions table")
            self.assertEqual(result['day_of_week'], 'TEST_E_Sunday')

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into excursions table: {e}")


    def test_excursions_required_fields_not_null(self):
        """Test that required fields (day_of_week, time, type) cannot be null"""
        # Try inserting data with NULL day_of_week
        with self.assertRaises((pymysql.err.IntegrityError, pymysql.err.OperationalError)):
            self.cursor.execute("INSERT INTO excursions (day_of_week, time, type) VALUES (NULL, '10:00:00', 'foot')")
            inserted_id = self.cursor.lastrowid # If insert succeeds unexpectedly
            self.created_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()

        # Try inserting data with NULL time
        with self.assertRaises((pymysql.err.IntegrityError, pymysql.err.OperationalError)):
            self.cursor.execute("INSERT INTO excursions (day_of_week, time, type) VALUES ('TEST_E_Day_Null', NULL, 'foot')")
            inserted_id = self.cursor.lastrowid
            self.created_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()

        # Try inserting data with NULL type
        with self.assertRaises((pymysql.err.IntegrityError, pymysql.err.OperationalError)):
            self.cursor.execute("INSERT INTO excursions (day_of_week, time, type) VALUES ('TEST_E_Day_Null', '10:00:00', NULL)")
            inserted_id = self.cursor.lastrowid
            self.created_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()


    def test_excursions_type_enum_values(self):
        """Test that the 'type' column only accepts ENUM values ('foot', 'vehicle')"""
        # Try inserting data with invalid type value
        with self.assertRaises(pymysql.err.DataError):
            self.cursor.execute("INSERT INTO excursions (day_of_week, time, type) VALUES ('TEST_E_Day_Invalid', '10:00:00', 'invalid')")
            inserted_id = self.cursor.lastrowid # If insert succeeds unexpectedly
            self.created_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()
