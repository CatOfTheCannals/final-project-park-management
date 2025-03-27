import unittest
import pymysql

class TestResearchProjectsDataRequirements(unittest.TestCase):
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

        # Insert a test natural element
        with cls.connection.cursor() as cursor:
            cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('Test Element', 'Test Common')")
            cls.connection.commit()
            # Get the element_id of the inserted record
            cursor.execute("SELECT id FROM natural_elements WHERE scientific_name = 'Test Element'")
            result = cursor.fetchone()
            cls.element_id = result['id']


    @classmethod
    def tearDownClass(cls):
        # Clean up test data
        with cls.connection.cursor() as cursor:
            # Delete projects first due to FK constraint in research_personnel (if any exist)
            cursor.execute("DELETE FROM research_projects WHERE element_id = %s", (cls.element_id,))
            cursor.execute("DELETE FROM natural_elements WHERE id = %s", (cls.element_id,))
        cls.connection.commit()
        cls.connection.close()

    def test_research_projects_table_exists(self):
        """Test that the research_projects table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'research_projects';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Research_projects table does not exist")

    def test_research_projects_has_required_columns(self):
        """Test that research_projects table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM research_projects LIKE 'id';")
        id_column = self.cursor.fetchone()
        self.assertIsNotNone(id_column, "Research_projects table does not have 'id' column")

        self.cursor.execute("SHOW COLUMNS FROM research_projects LIKE 'budget';")
        budget_column = self.cursor.fetchone()
        self.assertIsNotNone(budget_column, "Research_projects table does not have 'budget' column")

        self.cursor.execute("SHOW COLUMNS FROM research_projects LIKE 'duration';")
        duration_column = self.cursor.fetchone()
        self.assertIsNotNone(duration_column, "Research_projects table does not have 'duration' column")

        self.cursor.execute("SHOW COLUMNS FROM research_projects LIKE 'element_id';")
        element_id_column = self.cursor.fetchone()
        self.assertIsNotNone(element_id_column, "Research_projects table does not have 'element_id' column")

    def test_research_projects_foreign_key_constraint(self):
        """Test that research_projects table has foreign key constraint on element_id"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'research_projects' AND COLUMN_NAME = 'element_id'
            AND REFERENCED_TABLE_NAME = 'natural_elements';
        """)
        element_fk = self.cursor.fetchone()
        self.assertIsNotNone(element_fk, "Research_projects table does not have foreign key constraint on 'element_id'")


    def test_research_projects_data_insertion(self):
        """Test data insertion into research_projects table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO research_projects (budget, duration, element_id) VALUES (15000.00, '24 months', %s)", (self.element_id,))
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM research_projects WHERE budget = 15000.00")
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into research_projects table")

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into research_projects table: {e}")

        finally:
            # Clean up test data
            with self.connection.cursor() as cursor:
                # Use element_id for cleanup as budget might not be unique
                cursor.execute("DELETE FROM research_projects WHERE element_id = %s", (self.element_id,))
            self.connection.commit()

    def test_research_projects_required_fields_not_null(self):
        """Test that required fields (budget, duration, element_id) cannot be null"""
        try:
            # Try inserting data with NULL budget
            self.cursor.execute("INSERT INTO research_projects (budget, duration, element_id) VALUES (NULL, '12 months', %s)", (self.element_id,))
            self.connection.commit()
            self.fail("Should not allow NULL budget in research_projects table")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("cannot be null", str(e).lower(), "Error message does not indicate duration NULL constraint violation")

        try:
            # Try inserting data with NULL element_id
            self.cursor.execute("INSERT INTO research_projects (budget, duration, element_id) VALUES (13000.00, '18 months', NULL)")
            self.connection.commit()
            self.fail("Should not allow NULL element_id in research_projects table")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("cannot be null", str(e).lower(), "Error message does not indicate element_id NULL constraint violation")

    def test_research_projects_foreign_key_enforcement(self):
        """Test foreign key constraint enforcement in research_projects table"""
        try:
            # Try inserting invalid data (non-existent element_id)
            self.cursor.execute("INSERT INTO research_projects (budget, duration, element_id) VALUES (14000.00, '6 months', 99999)")
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent element_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate element_id foreign key constraint violation")

        try:
            # Try inserting data with NULL duration
            self.cursor.execute("INSERT INTO research_projects (budget, duration, element_id) VALUES (12000.00, NULL, %s)", (self.element_id,))
            self.connection.commit()
            self.fail("Should not allow NULL duration in research_projects table")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("cannot be null", str(e).lower(), "Error message does not indicate NULL constraint violation")
