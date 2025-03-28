import unittest
import pymysql

class TestSurveillancePersonnelDataRequirements(unittest.TestCase):
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
            cursor.execute("INSERT INTO personnel (DNI, CUIL, name, salary) VALUES ('TESTSP222', 'TESTSP20222', 'Test Surveillor', 50000.00)")
            self.personnel_id = cursor.lastrowid
            self.connection.commit()


    def tearDown(self):
        # Clean up test data
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM surveillance_personnel WHERE personnel_id = %s", (self.personnel_id,))
            cursor.execute("DELETE FROM personnel WHERE id = %s", (self.personnel_id,))
        self.connection.commit()
        self.connection.close()

    def test_surveillance_personnel_table_exists(self):
        """Test that the surveillance_personnel table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'surveillance_personnel';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Surveillance_personnel table does not exist")

    def test_surveillance_personnel_has_required_columns(self):
        """Test that surveillance_personnel table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM surveillance_personnel LIKE 'personnel_id';")
        personnel_id_column = self.cursor.fetchone()
        self.assertIsNotNone(personnel_id_column, "Surveillance_personnel table does not have 'personnel_id' column")

        self.cursor.execute("SHOW COLUMNS FROM surveillance_personnel LIKE 'vehicle_type';")
        vehicle_type_column = self.cursor.fetchone()
        self.assertIsNotNone(vehicle_type_column, "Surveillance_personnel table does not have 'vehicle_type' column")

        self.cursor.execute("SHOW COLUMNS FROM surveillance_personnel LIKE 'vehicle_registration';")
        vehicle_registration_column = self.cursor.fetchone()
        self.assertIsNotNone(vehicle_registration_column, "Surveillance_personnel table does not have 'vehicle_registration' column")

    def test_surveillance_personnel_foreign_key_constraint(self):
        """Test that surveillance_personnel table has foreign key constraint on personnel_id"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'surveillance_personnel' AND COLUMN_NAME = 'personnel_id'
            AND REFERENCED_TABLE_NAME = 'personnel';
        """)
        personnel_fk = self.cursor.fetchone()
        self.assertIsNotNone(personnel_fk, "Surveillance_personnel table does not have foreign key constraint on 'personnel_id'")

    def test_surveillance_personnel_data_insertion(self):
        """Test data insertion into surveillance_personnel table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO surveillance_personnel (personnel_id, vehicle_type, vehicle_registration) VALUES (%s, 'Truck', 'AB123CD')", (self.personnel_id,))
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM surveillance_personnel WHERE personnel_id = %s", (self.personnel_id,))
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into surveillance_personnel table")

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into surveillance_personnel table: {e}")

    def test_surveillance_personnel_foreign_key_enforcement(self):
        """Test foreign key constraint enforcement in surveillance_personnel table"""
        try:
            # Try inserting invalid data (non-existent personnel_id)
            self.cursor.execute("INSERT INTO surveillance_personnel (personnel_id, vehicle_type, vehicle_registration) VALUES (999, 'Truck', 'AB123CD')")
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent personnel_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate foreign key constraint violation")
