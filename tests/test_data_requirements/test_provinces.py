from unittest import TestCase
import pymysql


class TestProvincesDataRequirements(TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse the connection from previous tests
        cls.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='park_management',
            cursorclass=pymysql.cursors.DictCursor # Use DictCursor for easier access to column names
        )
        cls.cursor = cls.connection.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def test_provinces_table_exists(self):
        """Test that the provinces table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'provinces';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Provinces table does not exist")

    def test_provinces_has_required_columns(self):
        """Test that provinces table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM provinces LIKE 'name';")
        name_column = self.cursor.fetchone()
        self.assertIsNotNone(name_column, "Provinces table does not have 'name' column")

        self.cursor.execute("SHOW COLUMNS FROM provinces LIKE 'responsible_organization';")
        org_column = self.cursor.fetchone()
        self.assertIsNotNone(org_column, "Provinces table does not have 'responsible_organization' column")

    def test_provinces_responsible_organization_not_null(self):
        """Test that provinces table enforces NOT NULL constraint on responsible_organization"""
        try:
            # Try inserting a new province with a NULL responsible_organization
            self.cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('New Province', NULL);")
            self.connection.commit()
            self.fail("Should not allow NULL responsible_organization in provinces table")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("cannot be null", str(e).lower(), "Error message does not indicate NULL constraint violation")

    def test_provinces_responsible_organization_is_required(self):
        """Test that responsible_organization is required (NOT NULL and not empty)"""
        try:
            # Insert a province without a responsible organization (should fail due to NOT NULL)
            self.cursor.execute("INSERT INTO provinces (name) VALUES ('La Pampa')")
            self.connection.commit()
            self.fail("Should not allow a province without a responsible organization")
        except pymysql.err.IntegrityError:
            self.connection.rollback()

        try:
            # Insert a province with an empty responsible organization
            self.cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('San Luis', '')")
            self.connection.commit()
            self.fail("Should not allow a province with an empty responsible organization")
        except pymysql.err.IntegrityError:
            self.connection.rollback()
