import unittest
import pymysql

class TestResearchProjectsDataRequirements(unittest.TestCase):
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
        self.created_project_ids = [] # Track created project IDs

        # Insert a test natural element
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('TestElementRProj', 'CommonRProj')")
            self.element_id = cursor.lastrowid
            self.connection.commit()


    def tearDown(self):
        # Clean up test data
        with self.connection.cursor() as cursor:
            if self.created_project_ids:
                ids_format = ','.join(['%s'] * len(self.created_project_ids))
                # Delete from research_personnel first if any test creates links
                cursor.execute(f"DELETE FROM research_personnel WHERE project_id IN ({ids_format})", tuple(self.created_project_ids))
                cursor.execute(f"DELETE FROM research_projects WHERE id IN ({ids_format})", tuple(self.created_project_ids))
            # Delete the natural element created in setUp
            if self.element_id:
                cursor.execute("DELETE FROM natural_elements WHERE id = %s", (self.element_id,))
        self.connection.commit()
        self.connection.close()

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
            # Insert valid data
            self.cursor.execute("INSERT INTO research_projects (budget, duration, element_id) VALUES (15000.00, '24 months', %s)", (self.element_id,))
            inserted_id = self.cursor.lastrowid
            self.created_project_ids.append(inserted_id) # Track ID
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM research_projects WHERE id = %s", (inserted_id,))
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into research_projects table")
            self.assertEqual(result['budget'], 15000.00)

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into research_projects table: {e}")


    def test_research_projects_required_fields_not_null(self):
        """Test that required fields (budget, duration, element_id) cannot be null"""
        try:
        # Try inserting data with NULL budget
        with self.assertRaises((pymysql.err.IntegrityError, pymysql.err.OperationalError)):
            self.cursor.execute("INSERT INTO research_projects (budget, duration, element_id) VALUES (NULL, '12 months', %s)", (self.element_id,))
            inserted_id = self.cursor.lastrowid # If insert succeeds unexpectedly
            self.created_project_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()


        # Try inserting data with NULL duration
        with self.assertRaises((pymysql.err.IntegrityError, pymysql.err.OperationalError)):
            self.cursor.execute("INSERT INTO research_projects (budget, duration, element_id) VALUES (12000.00, NULL, %s)", (self.element_id,))
            inserted_id = self.cursor.lastrowid
            self.created_project_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()


        # Try inserting data with NULL element_id
        with self.assertRaises((pymysql.err.IntegrityError, pymysql.err.OperationalError)):
            self.cursor.execute("INSERT INTO research_projects (budget, duration, element_id) VALUES (13000.00, '18 months', NULL)")
            inserted_id = self.cursor.lastrowid
            self.created_project_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()


    def test_research_projects_foreign_key_enforcement(self):
        """Test foreign key constraint enforcement in research_projects table"""
        try:
        # Try inserting invalid data (non-existent element_id)
        with self.assertRaises(pymysql.err.IntegrityError):
            self.cursor.execute("INSERT INTO research_projects (budget, duration, element_id) VALUES (14000.00, '6 months', 99999)")
            inserted_id = self.cursor.lastrowid # If insert succeeds unexpectedly
            self.created_project_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()
