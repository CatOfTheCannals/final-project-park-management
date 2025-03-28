import unittest
import pymysql

class TestVisitorsDataRequirements(unittest.TestCase):
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
        self.park_id = None # Initialize
        self.accommodation_id = None # Initialize
        self.created_visitor_ids = [] # Track created visitor IDs

        # Insert dependencies: park, accommodation
        with self.connection.cursor() as cursor:
            # Park
            cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES ('Test Park V', '2024-01-01', 'testparkv@example.com', 'V', 100.00)")
            self.park_id = cursor.lastrowid

            # Accommodation
            cursor.execute("INSERT INTO accommodations (capacity, category) VALUES (4, 'TEST_V_Cabin')")
            self.accommodation_id = cursor.lastrowid
            self.connection.commit()


    def tearDown(self):
        # Clean up test data
        with self.connection.cursor() as cursor:
            if self.created_visitor_ids:
                 ids_format = ','.join(['%s'] * len(self.created_visitor_ids))
                 # Delete from linking tables first
                 cursor.execute(f"DELETE FROM visitor_excursions WHERE visitor_id IN ({ids_format})", tuple(self.created_visitor_ids))
                 cursor.execute(f"DELETE FROM visitors WHERE id IN ({ids_format})", tuple(self.created_visitor_ids))
            # Delete dependencies created in setUp
            cursor.execute("DELETE FROM accommodations WHERE id = %s", (self.accommodation_id,))
            cursor.execute("DELETE FROM parks WHERE id = %s", (self.park_id,))
        self.connection.commit()
        self.connection.close()

    def test_visitors_table_exists(self):
        """Test that the visitors table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'visitors';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Visitors table does not exist")

    def test_visitors_has_required_columns(self):
        """Test that visitors table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM visitors LIKE 'DNI';")
        dni_column = self.cursor.fetchone()
        self.assertIsNotNone(dni_column, "Visitors table does not have 'DNI' column")

        self.cursor.execute("SHOW COLUMNS FROM visitors LIKE 'name';")
        name_column = self.cursor.fetchone()
        self.assertIsNotNone(name_column, "Visitors table does not have 'name' column")

        self.cursor.execute("SHOW COLUMNS FROM visitors LIKE 'address';")
        address_column = self.cursor.fetchone()
        self.assertIsNotNone(address_column, "Visitors table does not have 'address' column")

        self.cursor.execute("SHOW COLUMNS FROM visitors LIKE 'profession';")
        profession_column = self.cursor.fetchone()
        self.assertIsNotNone(profession_column, "Visitors table does not have 'profession' column")

        self.cursor.execute("SHOW COLUMNS FROM visitors LIKE 'accommodation_id';")
        accommodation_id_column = self.cursor.fetchone()
        self.assertIsNotNone(accommodation_id_column, "Visitors table does not have 'accommodation_id' column")

        self.cursor.execute("SHOW COLUMNS FROM visitors LIKE 'park_id';")
        park_id_column = self.cursor.fetchone()
        self.assertIsNotNone(park_id_column, "Visitors table does not have 'park_id' column")

    def test_visitors_dni_unique(self):
        """Test that DNI is unique"""
        try:
            # Insert a visitor record
            self.cursor.execute("INSERT INTO visitors (DNI, name, accommodation_id, park_id) VALUES ('TESTV123', 'Test Name', %s, %s)", (self.accommodation_id, self.park_id))
            inserted_id_1 = self.cursor.lastrowid
            self.created_visitor_ids.append(inserted_id_1)
            self.connection.commit()

            # Try inserting another visitor record with the same DNI
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO visitors (DNI, name, accommodation_id, park_id) VALUES ('TESTV123', 'Another Name', %s, %s)", (self.accommodation_id, self.park_id))
                inserted_id_2 = self.cursor.lastrowid # If insert succeeds unexpectedly
                self.created_visitor_ids.append(inserted_id_2)
                self.connection.commit()
            self.connection.rollback()
        except Exception as e: # Catch any unexpected error during the setup/test itself
            self.fail(f"An unexpected error occurred in test_visitors_dni_unique: {e}")


    def test_visitors_data_insertion(self):
        self.connection.commit()

        # Try inserting another visitor record with the same DNI
        with self.assertRaises(pymysql.err.IntegrityError):
            self.cursor.execute("INSERT INTO visitors (DNI, name, accommodation_id, park_id) VALUES ('TESTV123', 'Another Name', %s, %s)", (self.accommodation_id, self.park_id))
            inserted_id_2 = self.cursor.lastrowid # If insert succeeds unexpectedly
            self.created_visitor_ids.append(inserted_id_2)
            self.connection.commit()
        self.connection.rollback()


    def test_visitors_data_insertion(self):
        """Test data insertion into visitors table"""
        try:
        # Insert valid data
        self.cursor.execute("INSERT INTO visitors (DNI, name, accommodation_id, park_id) VALUES ('TESTV987', 'Valid Name', %s, %s)", (self.accommodation_id, self.park_id))
        inserted_id = self.cursor.lastrowid
        self.created_visitor_ids.append(inserted_id)
        self.connection.commit()

        # Verify that the data was inserted
        self.cursor.execute("SELECT * FROM visitors WHERE id = %s", (inserted_id,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Data was not inserted into visitors table")
        self.assertEqual(result['DNI'], 'TESTV987')

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into visitors table: {e}")


    def test_visitors_required_fields_not_null(self):
        """Test that required fields (DNI, name) cannot be null"""
        try:
        # Try inserting data with NULL DNI
        with self.assertRaises((pymysql.err.IntegrityError, pymysql.err.OperationalError)):
            self.cursor.execute("INSERT INTO visitors (DNI, name, accommodation_id, park_id) VALUES (NULL, 'Null DNI Name', %s, %s)", (self.accommodation_id, self.park_id))
            inserted_id = self.cursor.lastrowid # If insert succeeds unexpectedly
            self.created_visitor_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()

        # Try inserting data with NULL name
        with self.assertRaises((pymysql.err.IntegrityError, pymysql.err.OperationalError)):
            self.cursor.execute("INSERT INTO visitors (DNI, name, accommodation_id, park_id) VALUES ('TESTV456', NULL, %s, %s)", (self.accommodation_id, self.park_id))
            inserted_id = self.cursor.lastrowid
            self.created_visitor_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()


    def test_visitors_foreign_key_constraint(self):
        """Test that visitors table has foreign key constraint on accommodation_id"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'visitors' AND COLUMN_NAME = 'accommodation_id'
            AND REFERENCED_TABLE_NAME = 'accommodations';
        """)
        accommodation_fk = self.cursor.fetchone()
        self.assertIsNotNone(accommodation_fk, "Visitors table does not have foreign key constraint on 'accommodation_id'")

        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'visitors' AND COLUMN_NAME = 'park_id'
            AND REFERENCED_TABLE_NAME = 'parks';
        """)
        park_fk = self.cursor.fetchone()
        self.assertIsNotNone(park_fk, "Visitors table does not have foreign key constraint on 'park_id'")

    def test_visitors_foreign_key_enforcement(self):
        """Test foreign key constraint enforcement in visitors table"""
        try:
        # Try inserting invalid data (non-existent accommodation_id)
        # Note: accommodation_id allows NULL, so this test might need adjustment if FK is strictly required
        if self.accommodation_id is not None: # Only test if accommodation_id is supposed to be valid
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO visitors (DNI, name, accommodation_id, park_id) VALUES ('TESTV555', 'Invalid Acc Name', 99999, %s)", (self.park_id,))
                inserted_id = self.cursor.lastrowid # If insert succeeds unexpectedly
                self.created_visitor_ids.append(inserted_id)
                self.connection.commit()
            self.connection.rollback()

        # Try inserting invalid data (non-existent park_id)
        with self.assertRaises(pymysql.err.IntegrityError):
            self.cursor.execute("INSERT INTO visitors (DNI, name, accommodation_id, park_id) VALUES ('TESTV666', 'Invalid Park Name', %s, 99999)", (self.accommodation_id,))
            inserted_id = self.cursor.lastrowid
            self.created_visitor_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()
