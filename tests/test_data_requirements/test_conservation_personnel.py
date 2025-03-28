import unittest
import pymysql

class TestConservationPersonnelDataRequirements(unittest.TestCase):
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
        self.park_id = None # Initialize
        self.area_number = 1 # Hardcoded for simplicity

        # Insert dependencies: personnel, park, park_area
        with self.connection.cursor() as cursor:
            # Personnel
            cursor.execute("INSERT INTO personnel (DNI, CUIL, name, salary) VALUES ('TESTCP444', 'TESTCP20444', 'Test Conservator', 50000.00)")
            self.personnel_id = cursor.lastrowid

            # Park
            cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES ('Test Park CP', '2024-01-01', 'testcp@example.com', 'CP', 100.00)")
            self.park_id = cursor.lastrowid

            # Park Area
            cursor.execute("INSERT INTO park_areas (park_id, area_number, name, extension) VALUES (%s, %s, 'Test Area CP', 100.00)", (self.park_id, self.area_number))
            self.connection.commit()


    def tearDown(self):
        # Clean up test data - order matters due to FKs
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM conservation_personnel WHERE personnel_id = %s", (self.personnel_id,))
            cursor.execute("DELETE FROM personnel WHERE id = %s", (self.personnel_id,))
            # Assuming no area_elements or park_provinces were created that depend on these
            cursor.execute("DELETE FROM park_areas WHERE park_id = %s AND area_number = %s", (self.park_id, self.area_number))
            cursor.execute("DELETE FROM parks WHERE id = %s", (self.park_id,))
        self.connection.commit()
        self.connection.close()

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

        self.cursor.execute("SHOW COLUMNS FROM conservation_personnel LIKE 'park_id';")
        park_id_column = self.cursor.fetchone()
        self.assertIsNotNone(park_id_column, "Conservation_personnel table does not have 'park_id' column")

        self.cursor.execute("SHOW COLUMNS FROM conservation_personnel LIKE 'area_number';")
        area_number_column = self.cursor.fetchone()
        self.assertIsNotNone(area_number_column, "Conservation_personnel table does not have 'area_number' column")


    def test_conservation_personnel_foreign_key_constraint(self):
        """Test that conservation_personnel table has foreign key constraints"""
        # Check FK on personnel_id
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'conservation_personnel' AND COLUMN_NAME = 'personnel_id'
            AND REFERENCED_TABLE_NAME = 'personnel';
        """)
        personnel_fk = self.cursor.fetchone()
        self.assertIsNotNone(personnel_fk, "Conservation_personnel table does not have foreign key constraint on 'personnel_id'")

        # Check composite FK on (park_id, area_number)
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'conservation_personnel' AND COLUMN_NAME = 'park_id'
            AND REFERENCED_TABLE_NAME = 'park_areas';
        """)
        park_area_fk_park = self.cursor.fetchone()
        self.assertIsNotNone(park_area_fk_park, "Conservation_personnel table does not have foreign key constraint on 'park_id' referencing park_areas")

        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'conservation_personnel' AND COLUMN_NAME = 'area_number'
            AND REFERENCED_TABLE_NAME = 'park_areas';
        """)
        park_area_fk_area = self.cursor.fetchone()
        self.assertIsNotNone(park_area_fk_area, "Conservation_personnel table does not have foreign key constraint on 'area_number' referencing park_areas")

        # Ensure both parts belong to the same constraint name
        self.assertEqual(park_area_fk_park['CONSTRAINT_NAME'], park_area_fk_area['CONSTRAINT_NAME'], "Composite foreign key on (park_id, area_number) seems incorrect")


    def test_conservation_personnel_data_insertion(self):
        """Test data insertion into conservation_personnel table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO conservation_personnel (personnel_id, specialty, park_id, area_number) VALUES (%s, 'Canine Care', %s, %s)", (self.personnel_id, self.park_id, self.area_number))
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
        # Test invalid personnel_id
        try:
            self.cursor.execute("INSERT INTO conservation_personnel (personnel_id, specialty, park_id, area_number) VALUES (999, 'Canine Care', %s, %s)", (self.park_id, self.area_number))
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent personnel_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate personnel_id foreign key constraint violation")

        # Test invalid park_id
        try:
            self.cursor.execute("INSERT INTO conservation_personnel (personnel_id, specialty, park_id, area_number) VALUES (%s, 'Canine Care', 999, %s)", (self.personnel_id, self.area_number))
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent park_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate park_id foreign key constraint violation")

        # Test invalid area_number (for the given park_id)
        try:
            self.cursor.execute("INSERT INTO conservation_personnel (personnel_id, specialty, park_id, area_number) VALUES (%s, 'Canine Care', %s, 999)", (self.personnel_id, self.park_id))
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent area_number for the park")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate area_number foreign key constraint violation")
