import unittest
import pymysql

class TestAccommodationExcursionsDataRequirements(unittest.TestCase):
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
        self.accommodation_id = None # Initialize
        self.excursion_id = None # Initialize

        # Insert dependencies: accommodation, excursion
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO accommodations (capacity, category) VALUES (4, 'TEST_AE_Cabin')")
            self.accommodation_id = cursor.lastrowid

            cursor.execute("INSERT INTO excursions (day_of_week, time, type) VALUES ('TEST_AE_Sunday', '10:00:00', 'foot')")
            self.excursion_id = cursor.lastrowid
            self.connection.commit()


    def tearDown(self):
        # Clean up test data - order matters
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM accommodation_excursions WHERE accommodation_id = %s AND excursion_id = %s", (self.accommodation_id, self.excursion_id))
            cursor.execute("DELETE FROM accommodations WHERE id = %s", (self.accommodation_id,))
            cursor.execute("DELETE FROM excursions WHERE id = %s", (self.excursion_id,))
        self.connection.commit()
        self.connection.close()

    def test_accommodation_excursions_table_exists(self):
        """Test that the accommodation_excursions table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'accommodation_excursions';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Accommodation_excursions table does not exist")

    def test_accommodation_excursions_has_required_columns(self):
        """Test that accommodation_excursions table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM accommodation_excursions LIKE 'accommodation_id';")
        accommodation_id_column = self.cursor.fetchone()
        self.assertIsNotNone(accommodation_id_column, "Accommodation_excursions table does not have 'accommodation_id' column")

        self.cursor.execute("SHOW COLUMNS FROM accommodation_excursions LIKE 'excursion_id';")
        excursion_id_column = self.cursor.fetchone()
        self.assertIsNotNone(excursion_id_column, "Accommodation_excursions table does not have 'excursion_id' column")

    def test_accommodation_excursions_foreign_key_constraints(self):
        """Test that accommodation_excursions table has foreign key constraints"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'accommodation_excursions' AND COLUMN_NAME = 'accommodation_id'
            AND REFERENCED_TABLE_NAME = 'accommodations';
        """)
        accommodation_fk = self.cursor.fetchone()
        self.assertIsNotNone(accommodation_fk, "Accommodation_excursions table does not have foreign key constraint on 'accommodation_id'")

        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'accommodation_excursions' AND COLUMN_NAME = 'excursion_id'
            AND REFERENCED_TABLE_NAME = 'excursions';
        """)
        excursion_fk = self.cursor.fetchone()
        self.assertIsNotNone(excursion_fk, "Accommodation_excursions table does not have foreign key constraint on 'excursion_id'")

    def test_accommodation_excursions_composite_primary_key(self):
        """Test that accommodation_excursions table has a composite primary key on accommodation_id and excursion_id"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
            WHERE TABLE_NAME = 'accommodation_excursions' AND CONSTRAINT_TYPE = 'PRIMARY KEY';
        """)
        primary_key = self.cursor.fetchone()
        self.assertIsNotNone(primary_key, "Accommodation_excursions table does not have a primary key")

        self.cursor.execute("""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'accommodation_excursions' AND CONSTRAINT_NAME = %s
            ORDER BY ORDINAL_POSITION;
        """, (primary_key['CONSTRAINT_NAME'],)) # Access by key for DictCursor
        primary_key_columns = [column['COLUMN_NAME'] for column in self.cursor.fetchall()] # Access by key
        # Order might vary, check presence and count
        self.assertIn('accommodation_id', primary_key_columns, "PK missing accommodation_id")
        self.assertIn('excursion_id', primary_key_columns, "PK missing excursion_id")
        self.assertEqual(len(primary_key_columns), 2, "PK should have exactly 2 columns")


    def test_accommodation_excursions_data_insertion(self):
        """Test data insertion into accommodation_excursions table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO accommodation_excursions (accommodation_id, excursion_id) VALUES (%s, %s)", (self.accommodation_id, self.excursion_id))
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM accommodation_excursions WHERE accommodation_id = %s AND excursion_id = %s", (self.accommodation_id, self.excursion_id))
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into accommodation_excursions table")

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into accommodation_excursions table: {e}")

    def test_accommodation_excursions_foreign_key_enforcement(self):
        """Test foreign key constraint enforcement in accommodation_excursions table"""
        try:
            # Try inserting invalid data (non-existent accommodation_id)
            self.cursor.execute("INSERT INTO accommodation_excursions (accommodation_id, excursion_id) VALUES (999, %s)", (self.excursion_id,))
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent accommodation_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate foreign key constraint violation")

        try:
            # Try inserting invalid data (non-existent excursion_id)
            self.cursor.execute("INSERT INTO accommodation_excursions (accommodation_id, excursion_id) VALUES (%s, 999)", (self.accommodation_id,))
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent excursion_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate foreign key constraint violation")
