import unittest
import pymysql

class TestConservationPersonnelDataRequirements(unittest.TestCase):
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

        # Insert a test personnel record
        with cls.connection.cursor() as cursor:
            cursor.execute("INSERT INTO personnel (DNI, CUIL, name, address, phone_numbers, salary) VALUES ('TEST44444444', 'TEST20444444444', 'Test Conservation Personnel', 'Test Address', '123-456-7890', 50000.00)")
            cls.connection.commit()

            # Get the personnel_id of the inserted record
            cursor.execute("SELECT id FROM personnel WHERE DNI = 'TEST44444444'")
            result = cursor.fetchone()
            cls.personnel_id = result['id']

    @classmethod
    def tearDownClass(cls):
        # Clean up test data
        with cls.connection.cursor() as cursor:
            cursor.execute("DELETE FROM conservation_personnel WHERE personnel_id = %s", (cls.personnel_id,))
            cursor.execute("DELETE FROM personnel WHERE DNI = 'TEST44444444'")
        cls.connection.commit()
        cls.connection.close()

    def test_conservation_personnel_table_exists(self):
        """Test that the conservation_personnel table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'conservation_personnel';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Conservation_personnel table does not exist")

    def test_conservation_personnel_has_required_columns(self):
        """Test that conservation_personnel table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM conservation_personnel LIKE 'personnel_id';")
        personnel_id_column = self.cursor.fetchone()
        self.assertIsNotNone(personnel_id_column, "Conservation_personnel table does not have 'personnel_id' column")

        self.cursor.execute("SHOW COLUMNS FROM conservation_personnel LIKE 'specialty';")
        specialty_column = self.cursor.fetchone()
        self.assertIsNotNone(specialty_column, "Conservation_personnel table does not have 'specialty' column")

    def test_conservation_personnel_foreign_key_constraint(self):
        """Test that conservation_personnel table has foreign key constraint on personnel_id"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'conservation_personnel' AND COLUMN_NAME = 'personnel_id'
            AND REFERENCED_TABLE_NAME = 'personnel';
        """)
        personnel_fk = self.cursor.fetchone()
        self.assertIsNotNone(personnel_fk, "Conservation_personnel table does not have foreign key constraint on 'personnel_id'")

    def test_conservation_personnel_data_insertion(self):
        """Test data insertion into conservation_personnel table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO conservation_personnel (personnel_id, specialty) VALUES (%s, 'Canine Care')", (self.personnel_id,))
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM conservation_personnel WHERE personnel_id = %s", (self.personnel_id,))
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into conservation_personnel table")

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into conservation_personnel table: {e}")

    def test_conservation_personnel_foreign_key_enforcement(self):
        """Test foreign key constraint enforcement in conservation_personnel table"""
        try:
            # Try inserting invalid data (non-existent personnel_id)
            self.cursor.execute("INSERT INTO conservation_personnel (personnel_id, specialty) VALUES (999, 'Canine Care')")
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent personnel_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate foreign key constraint violation")
