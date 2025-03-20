import unittest
import pymysql

class TestResearchPersonnelDataRequirements(unittest.TestCase):
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
            cursor.execute("INSERT INTO personnel (DNI, CUIL, name, address, phone_numbers, salary) VALUES ('TEST33333333', 'TEST20333333333', 'Test Research Personnel', 'Test Address', '123-456-7890', 50000.00)")
            cls.connection.commit()

            # Get the personnel_id of the inserted record
            cursor.execute("SELECT id FROM personnel WHERE DNI = 'TEST33333333'")
            result = cursor.fetchone()
            cls.personnel_id = result['id']

    @classmethod
    def tearDownClass(cls):
        # Clean up test data
        with cls.connection.cursor() as cursor:
            cursor.execute("DELETE FROM research_personnel WHERE personnel_id = %s", (cls.personnel_id,))
            cursor.execute("DELETE FROM personnel WHERE DNI = 'TEST33333333'")
        cls.connection.commit()
        cls.connection.close()

    def test_research_personnel_table_exists(self):
        """Test that the research_personnel table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'research_personnel';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Research_personnel table does not exist")

    def test_research_personnel_has_required_columns(self):
        """Test that research_personnel table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM research_personnel LIKE 'personnel_id';")
        personnel_id_column = self.cursor.fetchone()
        self.assertIsNotNone(personnel_id_column, "Research_personnel table does not have 'personnel_id' column")

        self.cursor.execute("SHOW COLUMNS FROM research_personnel LIKE 'title';")
        title_column = self.cursor.fetchone()
        self.assertIsNotNone(title_column, "Research_personnel table does not have 'title' column")

    def test_research_personnel_foreign_key_constraint(self):
        """Test that research_personnel table has foreign key constraint on personnel_id"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'research_personnel' AND COLUMN_NAME = 'personnel_id'
            AND REFERENCED_TABLE_NAME = 'personnel';
        """)
        personnel_fk = self.cursor.fetchone()
        self.assertIsNotNone(personnel_fk, "Research_personnel table does not have foreign key constraint on 'personnel_id'")

    def test_research_personnel_data_insertion(self):
        """Test data insertion into research_personnel table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO research_personnel (personnel_id, title) VALUES (%s, 'PhD in Biology')", (self.personnel_id,))
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM research_personnel WHERE personnel_id = %s", (self.personnel_id,))
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into research_personnel table")

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into research_personnel table: {e}")

    def test_research_personnel_foreign_key_enforcement(self):
        """Test foreign key constraint enforcement in research_personnel table"""
        try:
            # Try inserting invalid data (non-existent personnel_id)
            self.cursor.execute("INSERT INTO research_personnel (personnel_id, title) VALUES (999, 'PhD in Biology')")
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent personnel_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate foreign key constraint violation")
