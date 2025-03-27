import unittest
import pymysql

class TestVisitorsDataRequirements(unittest.TestCase):
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

        # Insert a test park record
        with cls.connection.cursor() as cursor:
            cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES ('Test Park for Visitors', '2024-01-01', 'testpark@example.com', 'VIS', 100.00)")
            cls.connection.commit()
            # Get the park_id of the inserted record
            cursor.execute("SELECT id FROM parks WHERE code = 'VIS'")
            result = cursor.fetchone()
            cls.park_id = result['id']

        # Insert a test accommodation record
        with cls.connection.cursor() as cursor:
            cursor.execute("INSERT INTO accommodations (capacity, category) VALUES (4, 'TEST Cabin')")
            cls.connection.commit()

            # Get the accommodation_id of the inserted record
            cursor.execute("SELECT id FROM accommodations WHERE category = 'TEST Cabin'")
            result = cursor.fetchone()
            cls.accommodation_id = result['id']

    @classmethod
    def tearDownClass(cls):
        # Clean up test data
        with cls.connection.cursor() as cursor:
            cursor.execute("DELETE FROM visitors WHERE DNI LIKE 'TEST%';")
            cursor.execute("DELETE FROM accommodations WHERE category LIKE 'TEST%';")
            cursor.execute("DELETE FROM parks WHERE code = 'VIS';") # Clean up test park
        cls.connection.commit()
        cls.connection.close()

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
            self.cursor.execute("INSERT INTO visitors (DNI, name, address, profession, accommodation_id, park_id) VALUES ('TEST12345678', 'Test Name', 'Test Address', 'Test Profession', %s, %s)", (self.accommodation_id, self.park_id))
            self.connection.commit()

            # Try inserting another visitor record with the same DNI
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO visitors (DNI, name, address, profession, accommodation_id, park_id) VALUES ('TEST12345678', 'Another Test Name', 'Another Test Address', 'Another Test Profession', %s, %s)", (self.accommodation_id, self.park_id))
                self.connection.commit()
            self.connection.rollback()

        finally:
            # Clean up the test data
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM visitors WHERE DNI LIKE 'TEST%';")
            self.connection.commit()

    def test_visitors_data_insertion(self):
        """Test data insertion into visitors table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO visitors (DNI, name, address, profession, accommodation_id, park_id) VALUES ('TEST98765432', 'Valid Name', 'Valid Address', 'Valid Profession', %s, %s)", (self.accommodation_id, self.park_id))
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM visitors WHERE DNI = 'TEST98765432'")
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into visitors table")

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into visitors table: {e}")

        finally:
            # Clean up the test data
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM visitors WHERE DNI LIKE 'TEST%';")
            self.connection.commit()

    def test_visitors_required_fields_not_null(self):
        """Test that required fields (DNI, name) cannot be null"""
        try:
            # Try inserting data with NULL DNI
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO visitors (DNI, name, address, profession, accommodation_id, park_id) VALUES (NULL, 'Null DNI Name', 'Null DNI Address', 'Null DNI Profession', %s, %s)", (self.accommodation_id, self.park_id))
                self.connection.commit()
            self.connection.rollback()

            # Try inserting data with NULL name
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO visitors (DNI, name, address, profession, accommodation_id, park_id) VALUES ('TEST45678901', NULL, 'Null Name Address', 'Null Name Profession', %s, %s)", (self.accommodation_id, self.park_id))
                self.connection.commit()
            self.connection.rollback()

        finally:
            # Clean up the test data
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM visitors WHERE DNI LIKE 'TEST%';")
            self.connection.commit()

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
            self.cursor.execute("INSERT INTO visitors (DNI, name, address, profession, accommodation_id, park_id) VALUES ('TEST55555555', 'Invalid Acc Name', 'Invalid Address', 'Invalid Profession', 999, %s)", (self.park_id,))
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent accommodation_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate accommodation_id foreign key constraint violation")

        try:
            # Try inserting invalid data (non-existent park_id)
            self.cursor.execute("INSERT INTO visitors (DNI, name, address, profession, accommodation_id, park_id) VALUES ('TEST66666666', 'Invalid Park Name', 'Invalid Address', 'Invalid Profession', %s, 999)", (self.accommodation_id,))
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent park_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate park_id foreign key constraint violation")
