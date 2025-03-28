import unittest
from unittest import TestCase
import pymysql


class TestParkProvincesDataRequirements(TestCase):
    # Use setUp and tearDown for test isolation
    def setUp(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='park_management',
            cursorclass=pymysql.cursors.DictCursor # Use DictCursor for consistency
        )
        self.cursor = self.connection.cursor()

        # Insert test province and park, getting IDs
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('TestProvPP', 'OrgPP');")
            self.province_id = cursor.lastrowid
            # Add the missing 'code' column
            cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES ('TestParkPP', '2020-01-01', 'parkpp@example.com', 'PP', 1000);")
            self.park_id = cursor.lastrowid
            self.connection.commit()

    def tearDown(self):
        with self.connection.cursor() as cursor:
            # Delete in reverse order of creation / dependency
            cursor.execute("DELETE FROM park_provinces WHERE park_id = %s", (self.park_id,))
            cursor.execute("DELETE FROM parks WHERE id = %s", (self.park_id,))
            cursor.execute("DELETE FROM provinces WHERE id = %s", (self.province_id,))
            # Clean up potential extra province from extension sum test
            cursor.execute("DELETE FROM provinces WHERE name = 'CordobaPPTest';")
        self.connection.commit()
        self.connection.close()

    def test_park_provinces_table_exists(self):
        """Test that the park_provinces table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'park_provinces';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Park_provinces table does not exist")

    def test_park_provinces_has_required_columns(self):
        """Test that park_provinces table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM park_provinces LIKE 'park_id';")
        park_id_column = self.cursor.fetchone()
        self.assertIsNotNone(park_id_column, "Park_provinces table does not have 'park_id' column")

        self.cursor.execute("SHOW COLUMNS FROM park_provinces LIKE 'province_id';")
        province_id_column = self.cursor.fetchone()
        self.assertIsNotNone(province_id_column, "Park_provinces table does not have 'province_id' column")

        self.cursor.execute("SHOW COLUMNS FROM park_provinces LIKE 'extension_in_province';")
        extension_in_province_column = self.cursor.fetchone()
        self.assertIsNotNone(extension_in_province_column, "Park_provinces table does not have 'extension_in_province' column")

    def test_park_provinces_foreign_key_constraints(self):
        """Test that park_provinces table has foreign key constraints"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'park_provinces' AND COLUMN_NAME = 'park_id'
            AND REFERENCED_TABLE_NAME = 'parks';
        """)
        park_fk = self.cursor.fetchone()
        self.assertIsNotNone(park_fk, "Park_provinces table does not have foreign key constraint on 'park_id'")

        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'park_provinces' AND COLUMN_NAME = 'province_id'
            AND REFERENCED_TABLE_NAME = 'provinces';
        """)
        province_fk = self.cursor.fetchone()
        self.assertIsNotNone(province_fk, "Park_provinces table does not have foreign key constraint on 'province_id'")

    def test_park_provinces_composite_primary_key(self):
        """Test that park_provinces table has a composite primary key on park_id and province_id"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
            WHERE TABLE_NAME = 'park_provinces' AND CONSTRAINT_TYPE = 'PRIMARY KEY';
        """)
        primary_key = self.cursor.fetchone()
        self.assertIsNotNone(primary_key, "Park_provinces table does not have a primary key")

        self.cursor.execute("""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'park_provinces' AND CONSTRAINT_NAME = %s
            ORDER BY ORDINAL_POSITION;
        """, (primary_key['CONSTRAINT_NAME'],)) # Access by key
        primary_key_columns = [column['COLUMN_NAME'] for column in self.cursor.fetchall()] # Access by key
        # Order might vary, check presence and count
        self.assertIn('park_id', primary_key_columns, "PK missing park_id")
        self.assertIn('province_id', primary_key_columns, "PK missing province_id")
        self.assertEqual(len(primary_key_columns), 2, "PK should have exactly 2 columns")


    def test_park_provinces_data_insertion(self):
        """Test data insertion into park_provinces table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, %s, 500.00)", (self.park_id, self.province_id))
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM park_provinces WHERE park_id = %s AND province_id = %s", (self.park_id, self.province_id))
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into park_provinces table")

        except Exception as e:
            self.connection.rollback()
            self.connection.rollback()
            self.fail(f"Error inserting data into park_provinces table: {e}")
        finally:
             # Clean up inserted data for this specific test
            self.cursor.execute("DELETE FROM park_provinces WHERE park_id = %s AND province_id = %s", (self.park_id, self.province_id))
            self.connection.commit()


    # This test seems misplaced, belongs in test_provinces.py
    # def test_required_fields_are_enforced(self):
    #     """Test that required fields cannot be null"""
    #     try:
    #         # Try inserting invalid data into provinces table
    #         self.cursor.execute("INSERT INTO provinces (name) VALUES (NULL);")
    #         self.fail("Should not allow NULL name in provinces table")
    #     except pymysql.err.IntegrityError:
    #         self.connection.rollback() # Rollback the transaction

    def test_park_provinces_extension_sum_equals_park_total_extension(self):
        """Test that the sum of extension_in_province for a park equals the park's total_extension"""
        cordoba_id = None # Define in outer scope
        try:
            # Insert first part for the park (using self.province_id)
            self.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, %s, 600.00)", (self.park_id, self.province_id))

            # Insert a second province for the test
            self.cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('CordobaPPTest', 'Secretaria Ambiente');")
            cordoba_id = self.cursor.lastrowid

            # Insert second part for the park
            self.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, %s, 400.00)", (self.park_id, cordoba_id))
            self.connection.commit()

            # Calculate the sum of extension_in_province for the park
            self.cursor.execute("SELECT SUM(extension_in_province) as total_prov_extension FROM park_provinces WHERE park_id = %s", (self.park_id,))
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "SUM query returned no result")
            sum_extension_in_province = result['total_prov_extension'] # Access by alias

            # Get the total_area of the park
            self.cursor.execute("SELECT total_area FROM parks WHERE id = %s", (self.park_id,))
            total_area = self.cursor.fetchone()['total_area'] # Access by key

            # Assert that the sum of extension_in_province equals the total_area
            # Use assertAlmostEqual for floating point comparisons
            self.assertAlmostEqual(float(sum_extension_in_province), float(total_area), places=2, msg="Sum of extension_in_province does not equal park's total_area")
        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error in test_park_provinces_extension_sum_equals_park_total_extension: {e}")
        finally:
            # Clean up data specific to this test
            if cordoba_id:
                self.cursor.execute("DELETE FROM park_provinces WHERE province_id = %s", (cordoba_id,))
                self.cursor.execute("DELETE FROM provinces WHERE id = %s", (cordoba_id,))
            self.cursor.execute("DELETE FROM park_provinces WHERE park_id = %s AND province_id = %s", (self.park_id, self.province_id))
            self.connection.commit()


    def test_park_provinces_foreign_key_enforcement(self):
        """Test foreign key constraint enforcement in park_provinces table"""
        try:
            # Try inserting invalid data (non-existent park_id)
            self.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (999, %s, 100)", (self.province_id,))
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent park_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate foreign key constraint violation")

        try:
            # Try inserting invalid data (non-existent province_id)
            self.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, 999, 100)", (self.park_id,))
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent province_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate foreign key constraint violation")
