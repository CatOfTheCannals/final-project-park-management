import unittest
import pymysql

class TestResearchPersonnelDataRequirements(unittest.TestCase):
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
        self.element_id = None # Initialize
        self.project_id = None # Initialize
        self.personnel_id = None # Initialize

        # Insert dependencies: natural_element, research_project, personnel
        with self.connection.cursor() as cursor:
            # Element
            cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('TestElementRP', 'CommonRP');")
            self.element_id = cursor.lastrowid

            # Project (add missing element_id)
            cursor.execute("INSERT INTO research_projects (budget, duration, element_id) VALUES (10000.00, '12 months', %s)", (self.element_id,))
            self.project_id = cursor.lastrowid

            # Personnel
            cursor.execute("INSERT INTO personnel (DNI, CUIL, name, salary) VALUES ('TESTRP333', 'TESTRP20333', 'Test Researcher', 50000.00)")
            self.personnel_id = cursor.lastrowid
            self.connection.commit()


    def tearDown(self):
        # Clean up test data - order matters
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM research_personnel WHERE personnel_id = %s", (self.personnel_id,))
            cursor.execute("DELETE FROM personnel WHERE id = %s", (self.personnel_id,))
            cursor.execute("DELETE FROM research_projects WHERE id = %s", (self.project_id,))
            cursor.execute("DELETE FROM natural_elements WHERE id = %s", (self.element_id,))
        self.connection.commit()
        self.connection.close()

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

        self.cursor.execute("SHOW COLUMNS FROM research_personnel LIKE 'project_id';")
        project_id_column = self.cursor.fetchone()
        self.assertIsNotNone(project_id_column, "Research_personnel table does not have 'project_id' column")

    def test_research_personnel_foreign_key_constraint(self):
        """Test that research_personnel table has foreign key constraint on personnel_id"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'research_personnel' AND COLUMN_NAME = 'personnel_id'
            AND REFERENCED_TABLE_NAME = 'personnel';
        """)
        personnel_fk = self.cursor.fetchone()
        self.assertIsNotNone(personnel_fk, "Research_personnel table does not have foreign key constraint on 'personnel_id'")

        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'research_personnel' AND COLUMN_NAME = 'project_id'
            AND REFERENCED_TABLE_NAME = 'research_projects';
        """)
        project_fk = self.cursor.fetchone()
        self.assertIsNotNone(project_fk, "Research_personnel table does not have foreign key constraint on 'project_id'")

    def test_research_personnel_data_insertion(self):
        """Test data insertion into research_personnel table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO research_personnel (personnel_id, title, project_id) VALUES (%s, 'PhD in Biology', %s)", (self.personnel_id, self.project_id))
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
            self.cursor.execute("INSERT INTO research_personnel (personnel_id, title, project_id) VALUES (999, 'PhD in Biology', %s)", (self.project_id,))
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent personnel_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate foreign key constraint violation")

        try:
            # Try inserting invalid data (non-existent project_id)
            self.cursor.execute("INSERT INTO research_personnel (personnel_id, title, project_id) VALUES (%s, 'PhD in Biology', 999)", (self.personnel_id,))
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent project_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate foreign key constraint violation")
