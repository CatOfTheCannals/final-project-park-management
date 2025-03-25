from unittest import TestCase
import pymysql


class TestParkProvincesDataRequirements(TestCase):
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

        # Insert some test data
        with cls.connection.cursor() as cursor:
            cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('Buenos Aires', 'OPDS');")
            cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, total_area) VALUES ('Parque A', '2020-01-01', 'parqueA@example.com', 1000);")
            cls.connection.commit()

        # Get the IDs of the inserted province and park
        with cls.connection.cursor() as cursor:
            cursor.execute("SELECT id FROM provinces WHERE name = 'Buenos Aires';")
            cls.province_id = cursor.fetchone()['id']
            cursor.execute("SELECT id FROM parks WHERE name = 'Parque A';")
            cls.park_id = cursor.fetchone()['id']

    @classmethod
    def tearDownClass(cls):
        with cls.connection.cursor() as cursor:
            cursor.execute("DELETE FROM park_provinces WHERE park_id = %s AND province_id = %s", (cls.park_id, cls.province_id))
            cursor.execute("DELETE FROM provinces WHERE name = 'Buenos Aires';")
            cursor.execute("DELETE FROM parks WHERE name = 'Parque A';")
        cls.connection.commit()
        cls.connection.close()

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
        """, (primary_key[0],))
        primary_key_columns = [column[0] for column in self.cursor.fetchall()]
        self.assertEqual(primary_key_columns, ['park_id', 'province_id'], "Park_provinces table does not have a composite primary key on park_id and province_id")

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
            self.fail(f"Error inserting data into park_provinces table: {e}")

    def required_fields_are_enforced(self):
        """Test that required fields cannot be null"""
        try:
            # Try inserting invalid data into provinces table
            self.cursor.execute("INSERT INTO provinces (name) VALUES (NULL);")
            self.fail("Should not allow NULL name in provinces table")
        except pymysql.err.IntegrityError:
            self.connection.rollback() # Rollback the transaction

    def test_park_provinces_extension_sum_equals_park_total_extension(self):
        """Test that the sum of extension_in_province for a park equals the park's total_extension"""
        try:
            # Insert data for two provinces sharing the same park
            self.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, %s, 600.00)", (self.park_id, self.province_id))
            self.cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('Cordoba', 'Secretaria de Ambiente');")
            self.connection.commit()
            self.cursor.execute("SELECT id FROM provinces WHERE name = 'Cordoba';")
            cordoba_id = self.cursor.fetchone()['id']
            self.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, %s, 400.00)", (self.park_id, cordoba_id))
            self.connection.commit()

            # Calculate the sum of extension_in_province for the park
            self.cursor.execute("SELECT SUM(extension_in_province) FROM park_provinces WHERE park_id = %s", (self.park_id,))
            sum_extension_in_province = self.cursor.fetchone()[0]

            # Get the total_area of the park
            self.cursor.execute("SELECT total_area FROM parks WHERE id = %s", (self.park_id,))
            total_area = self.cursor.fetchone()[0]

            # Assert that the sum of extension_in_province equals the total_area
            self.assertEqual(float(sum_extension_in_province), float(total_area), "Sum of extension_in_province does not equal park's total_area")
        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error in test_park_provinces_extension_sum_equals_park_total_extension: {e}")

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
