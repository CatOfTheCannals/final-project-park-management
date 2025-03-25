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

    @classmethod
    def tearDownClass(cls):
        # Clean up test data
        with cls.connection.cursor() as cursor:
            cursor.execute("DELETE FROM research_projects WHERE budget LIKE 'TEST%';")
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

    def test_research_projects_data_insertion(self):
        """Test data insertion into research_projects table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO research_projects (budget, duration) VALUES (15000.00, '24 months')")
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
                cursor.execute("DELETE FROM research_projects WHERE budget LIKE 'TEST%';")
            self.connection.commit()

    def test_research_projects_required_fields_not_null(self):
        """Test that required fields (budget, duration) cannot be null"""
        try:
            # Try inserting data with NULL budget
            self.cursor.execute("INSERT INTO research_projects (budget, duration) VALUES (NULL, '12 months')")
            self.connection.commit()
            self.fail("Should not allow NULL budget in research_projects table")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("cannot be null", str(e).lower(), "Error message does not indicate NULL constraint violation")

        try:
            # Try inserting data with NULL duration
            self.cursor.execute("INSERT INTO research_projects (budget, duration) VALUES (12000.00, NULL)")
            self.connection.commit()
            self.fail("Should not allow NULL duration in research_projects table")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("cannot be null", str(e).lower(), "Error message does not indicate NULL constraint violation")
