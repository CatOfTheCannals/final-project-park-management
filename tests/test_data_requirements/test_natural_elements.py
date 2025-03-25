from unittest import TestCase
import pymysql


class TestNaturalElementsDataRequirements(TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse the connection from previous tests
        cls.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='park_management'
        )
        cls.cursor = cls.connection.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def natural_elements_table_exists(self):
        """Test that the natural_elements table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'natural_elements';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Natural elements table does not exist")

    def natural_elements_has_required_columns(self):
        """Test that natural_elements table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM natural_elements LIKE 'scientific_name';")
        scientific_name_column = self.cursor.fetchone()
        self.assertIsNotNone(scientific_name_column, "Natural elements table does not have 'scientific_name' column")

        self.cursor.execute("SHOW COLUMNS FROM natural_elements LIKE 'common_name';")
        common_name_column = self.cursor.fetchone()
        self.assertIsNotNone(common_name_column, "Natural elements table does not have 'common_name' column")

class TestAreaDataRequirements(TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse the connection from previous tests
        cls.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='park_management'
        )
        cls.cursor = cls.connection.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def area_elements_table_exists(self):
        """Test that the area_elements table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'area_elements';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Area elements table does not exist")

    def area_elements_has_required_columns(self):
        """Test that area_elements table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM area_elements LIKE 'park_id';")
        park_id_column = self.cursor.fetchone()
        self.assertIsNotNone(park_id_column, "Area elements table does not have 'park_id' column")

        self.cursor.execute("SHOW COLUMNS FROM area_elements LIKE 'area_number';")
        area_number_column = self.cursor.fetchone()
        self.assertIsNotNone(area_number_column, "Area elements table does not have 'area_number' column")

        self.cursor.execute("SHOW COLUMNS FROM area_elements LIKE 'element_id';")
        element_id_column = self.cursor.fetchone()
        self.assertIsNotNone(element_id_column, "Area elements table does not have 'element_id' column")

        self.cursor.execute("SHOW COLUMNS FROM area_elements LIKE 'number_of_individuals';")
        number_of_individuals_column = self.cursor.fetchone()
        self.assertIsNotNone(number_of_individuals_column, "Area elements table does not have 'number_of_individuals' column")

    def area_elements_has_foreign_key_constraints(self):
        """Test that area_elements table has foreign key constraints"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'area_elements' AND COLUMN_NAME = 'park_id'
            AND REFERENCED_TABLE_NAME = 'park_areas';
        """)
        park_fk = self.cursor.fetchone()
        self.assertIsNotNone(park_fk, "Area elements table does not have foreign key constraint on 'park_id'")

        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'area_elements' AND COLUMN_NAME = 'area_number'
            AND REFERENCED_TABLE_NAME = 'park_areas';
        """)
        area_number_fk = self.cursor.fetchone()
        self.assertIsNotNone(area_number_fk, "Area elements table does not have foreign key constraint on 'area_number'")

        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'area_elements' AND COLUMN_NAME = 'element_id'
            AND REFERENCED_TABLE_NAME = 'natural_elements';
        """)
        element_fk = self.cursor.fetchone()
        self.assertIsNotNone(element_fk, "Area elements table does not have foreign key constraint on 'element_id'")

    def area_elements_composite_primary_key(self):
        """Test that area_elements table has a composite primary key on park_id, area_number and element_id"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
            WHERE TABLE_NAME = 'area_elements' AND CONSTRAINT_TYPE = 'PRIMARY KEY';
        """)
        primary_key = self.cursor.fetchone()
        self.assertIsNotNone(primary_key, "Area elements table does not have a primary key")

        self.cursor.execute("""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'area_elements' AND CONSTRAINT_NAME = %s
            ORDER BY ORDINAL_POSITION;
        """, (primary_key[0],))
        primary_key_columns = [column[0] for column in self.cursor.fetchall()]
        self.assertEqual(primary_key_columns, ['park_id', 'area_number', 'element_id'], "Area elements table does not have a composite primary key on park_id, area_number and element_id")
