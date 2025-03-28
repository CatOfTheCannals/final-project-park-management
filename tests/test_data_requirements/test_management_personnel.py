import unittest
import pymysql

class TestManagementPersonnelDataRequirements(unittest.TestCase):
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
        self.personnel_id = None # Initialize

        # Insert a test personnel record
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO personnel (DNI, CUIL, name, salary) VALUES ('TESTMP111', 'TESTMP20111', 'Test Manager', 50000.00)")
            self.personnel_id = cursor.lastrowid
            self.connection.commit()


    def tearDown(self):
        # Clean up test data
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM management_personnel WHERE personnel_id = %s", (self.personnel_id,))
            cursor.execute("DELETE FROM personnel WHERE id = %s", (self.personnel_id,))
        self.connection.commit()
        self.connection.close()

    def test_management_personnel_table_exists(self):
        """Test that the management_personnel table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'management_personnel';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Management_personnel table does not exist")

    def test_management_personnel_has_required_columns(self):
        """Test that management_personnel table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM management_personnel LIKE 'personnel_id';")
        personnel_id_column = self.cursor.fetchone()
        self.assertIsNotNone(personnel_id_column, "Management_personnel table does not have 'personnel_id' column")

        self.cursor.execute("SHOW COLUMNS FROM management_personnel LIKE 'entrance_number';")
        entrance_number_column = self.cursor.fetchone()
        self.assertIsNotNone(entrance_number_column, "Management_personnel table does not have 'entrance_number' column")

    def test_management_personnel_foreign_key_constraint(self):
        """Test that management_personnel table has foreign key constraint on personnel_id"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'management_personnel' AND COLUMN_NAME = 'personnel_id'
            AND REFERENCED_TABLE_NAME = 'personnel';
        """)
        personnel_fk = self.cursor.fetchone()
        self.assertIsNotNone(personnel_fk, "Management_personnel table does not have foreign key constraint on 'personnel_id'")

    def test_management_personnel_data_insertion(self):
        """Test data insertion into management_personnel table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO management_personnel (personnel_id, entrance_number) VALUES (%s, 1)", (self.personnel_id,))
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM management_personnel WHERE personnel_id = %s", (self.personnel_id,))
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into management_personnel table")

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into management_personnel table: {e}")

    def test_management_personnel_foreign_key_enforcement(self):
        """Test foreign key constraint enforcement in management_personnel table"""
        try:
            # Try inserting invalid data (non-existent personnel_id)
            self.cursor.execute("INSERT INTO management_personnel (personnel_id, entrance_number) VALUES (999, 1)")
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent personnel_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate foreign key constraint violation")
