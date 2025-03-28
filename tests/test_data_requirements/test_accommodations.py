import unittest
import pymysql

class TestAccommodationsDataRequirements(unittest.TestCase):
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
        # Keep track of IDs created during tests
        self.created_ids = []

    def tearDown(self):
        # Clean up test data created during tests
        if self.created_ids:
            with self.connection.cursor() as cursor:
                # Format IDs for the IN clause
                ids_format = ','.join(['%s'] * len(self.created_ids))
                cursor.execute(f"DELETE FROM accommodations WHERE id IN ({ids_format})", tuple(self.created_ids))
            self.connection.commit()
        self.connection.close()

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
            # Insert valid data
            self.cursor.execute("INSERT INTO accommodations (capacity, category) VALUES (4, 'TEST_A_Cabin')")
            inserted_id = self.cursor.lastrowid
            self.created_ids.append(inserted_id) # Track created ID
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM accommodations WHERE id = %s", (inserted_id,))
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into accommodations table")
            self.assertEqual(result['category'], 'TEST_A_Cabin')

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into accommodations table: {e}")


    def test_accommodations_required_fields_not_null(self):
        """Test that required fields (capacity) cannot be null"""
        # Try inserting data with NULL capacity
        with self.assertRaises((pymysql.err.IntegrityError, pymysql.err.OperationalError)): # Catch both potential errors
            self.cursor.execute("INSERT INTO accommodations (capacity, category) VALUES (NULL, 'TEST_A_Category_Null')")
            # If insert succeeds unexpectedly, track ID for cleanup
            inserted_id = self.cursor.lastrowid
            self.created_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback() # Rollback after expected error
