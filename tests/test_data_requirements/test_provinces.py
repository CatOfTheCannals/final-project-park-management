import unittest
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
        # Catch OperationalError as well, as strict mode might be off
        except (pymysql.err.IntegrityError, pymysql.err.OperationalError) as e:
            self.connection.rollback()
            # Check for common messages indicating a NOT NULL violation
            error_msg = str(e).lower()
            self.assertTrue("cannot be null" in error_msg or "doesn't have a default value" in error_msg,
                            f"Error message does not indicate NULL constraint violation: {error_msg}")
        finally:
            # Clean up potentially inserted data
            self.cursor.execute("DELETE FROM provinces WHERE name = 'New Province';")
            self.connection.commit()


    def test_provinces_responsible_organization_is_required(self):
        """Test that responsible_organization is required (NOT NULL)"""
        try:
            # Insert a province without a responsible organization (should fail due to NOT NULL)
            self.cursor.execute("INSERT INTO provinces (name) VALUES ('TestProvRequired')")
            self.connection.commit()
            self.fail("Should not allow a province without a responsible organization")
        # Catch OperationalError as well, as strict mode might be off
        except (pymysql.err.IntegrityError, pymysql.err.OperationalError) as e:
            self.connection.rollback()
            # Check for common messages indicating a NOT NULL violation
            error_msg = str(e).lower()
            self.assertTrue("cannot be null" in error_msg or "doesn't have a default value" in error_msg,
                            f"Error message does not indicate NULL constraint violation: {error_msg}")
        finally:
            # Clean up potentially inserted data
            self.cursor.execute("DELETE FROM provinces WHERE name = 'TestProvRequired';")
            self.connection.commit()

        # Note: Inserting an empty string '' IS generally allowed by NOT NULL constraint.
        # If empty strings should be disallowed, a CHECK constraint or trigger is needed.
        # try:
        #     # Insert a province with an empty responsible organization
        #     self.cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('TestProvEmptyOrg', '')")
        #     self.connection.commit()
        #     # self.fail("Should not allow a province with an empty responsible organization") # This check is likely incorrect for NOT NULL
        # except (pymysql.err.IntegrityError, pymysql.err.OperationalError):
        #     self.connection.rollback()
        # finally:
        #     # Clean up potentially inserted data
        #     self.cursor.execute("DELETE FROM provinces WHERE name = 'TestProvEmptyOrg';")
        #     self.connection.commit()
