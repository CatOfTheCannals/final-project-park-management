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

        # Insert a test park and area
        with cls.connection.cursor() as cursor:
            cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES ('Test Park Cons', '2024-01-01', 'testcons@example.com', 'CONS', 100.00)")
            cls.connection.commit()
            cursor.execute("SELECT id FROM parks WHERE code = 'CONS'")
            cls.park_id = cursor.fetchone()['id']

            cursor.execute("INSERT INTO park_areas (park_id, area_number, name, extension) VALUES (%s, 1, 'Test Area Cons', 100.00)", (cls.park_id,))
            cls.connection.commit()
            cls.area_number = 1 # Hardcoded for simplicity

    @classmethod
    def tearDownClass(cls):
        # Clean up test data - order matters due to FKs
        with cls.connection.cursor() as cursor:
            cursor.execute("DELETE FROM conservation_personnel WHERE personnel_id = %s", (cls.personnel_id,))
            cursor.execute("DELETE FROM personnel WHERE DNI = 'TEST44444444'")
            # Need to delete area_elements if any were linked to this area before deleting park_areas
            # cursor.execute("DELETE FROM area_elements WHERE park_id = %s AND area_number = %s", (cls.park_id, cls.area_number))
            cursor.execute("DELETE FROM park_areas WHERE park_id = %s AND area_number = %s", (cls.park_id, cls.area_number))
            # Need to delete park_provinces if any were linked before deleting parks
            # cursor.execute("DELETE FROM park_provinces WHERE park_id = %s", (cls.park_id,))
            cursor.execute("DELETE FROM parks WHERE id = %s", (cls.park_id,))
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
