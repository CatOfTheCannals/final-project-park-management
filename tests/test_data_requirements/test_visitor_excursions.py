import unittest
import pymysql

class TestVisitorExcursionsDataRequirements(unittest.TestCase):
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

        # Insert a test park record (needed for visitor)
        with cls.connection.cursor() as cursor:
            cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES ('Test Park VE', '2024-01-01', 'testve@example.com', 'VE', 100.00) ON DUPLICATE KEY UPDATE code=code;")
            cls.connection.commit()
            cursor.execute("SELECT id FROM parks WHERE code = 'VE'")
            cls.park_id = cursor.fetchone()['id']

        # Insert a test visitor record
        with cls.connection.cursor() as cursor:
            # Need accommodation first if visitor FK requires it (it's SET NULL, so optional)
            # cursor.execute("INSERT INTO accommodations (capacity, category) VALUES (2, 'VE Cabin') ON DUPLICATE KEY UPDATE category=category;")
            # cls.connection.commit()
            # cursor.execute("SELECT id FROM accommodations WHERE category = 'VE Cabin'")
            # cls.accommodation_id = cursor.fetchone()['id']

            cursor.execute("INSERT INTO visitors (DNI, name, park_id) VALUES ('TESTVE123', 'Test Visitor VE', %s) ON DUPLICATE KEY UPDATE DNI=DNI;", (cls.park_id,))
            cls.connection.commit()
            cursor.execute("SELECT id FROM visitors WHERE DNI = 'TESTVE123'")
            cls.visitor_id = cursor.fetchone()['id']

        # Insert a test excursion record
        with cls.connection.cursor() as cursor:
            cursor.execute("INSERT INTO excursions (day_of_week, time, type) VALUES ('TEST Monday VE', '09:00:00', 'vehicle') ON DUPLICATE KEY UPDATE day_of_week=day_of_week;")
            cls.connection.commit()
            cursor.execute("SELECT id FROM excursions WHERE day_of_week = 'TEST Monday VE'")
            cls.excursion_id = cursor.fetchone()['id']

    @classmethod
    def tearDownClass(cls):
        # Clean up test data - order matters
        with cls.connection.cursor() as cursor:
            cursor.execute("DELETE FROM visitor_excursions WHERE visitor_id = %s AND excursion_id = %s", (cls.visitor_id, cls.excursion_id))
            cursor.execute("DELETE FROM visitors WHERE id = %s", (cls.visitor_id,))
            # cursor.execute("DELETE FROM accommodations WHERE category = 'VE Cabin';") # If accommodation was created
            cursor.execute("DELETE FROM excursions WHERE id = %s", (cls.excursion_id,))
            cursor.execute("DELETE FROM parks WHERE id = %s", (cls.park_id,))
        cls.connection.commit()
        cls.connection.close()

    def test_visitor_excursions_table_exists(self):
        """Test that the visitor_excursions table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'visitor_excursions';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Visitor_excursions table does not exist")

    def test_visitor_excursions_has_required_columns(self):
        """Test that visitor_excursions table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM visitor_excursions LIKE 'visitor_id';")
        visitor_id_column = self.cursor.fetchone()
        self.assertIsNotNone(visitor_id_column, "Visitor_excursions table does not have 'visitor_id' column")

        self.cursor.execute("SHOW COLUMNS FROM visitor_excursions LIKE 'excursion_id';")
        excursion_id_column = self.cursor.fetchone()
        self.assertIsNotNone(excursion_id_column, "Visitor_excursions table does not have 'excursion_id' column")

    def test_visitor_excursions_foreign_key_constraints(self):
        """Test that visitor_excursions table has foreign key constraints"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'visitor_excursions' AND COLUMN_NAME = 'visitor_id'
            AND REFERENCED_TABLE_NAME = 'visitors';
        """)
        visitor_fk = self.cursor.fetchone()
        self.assertIsNotNone(visitor_fk, "Visitor_excursions table does not have foreign key constraint on 'visitor_id'")

        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'visitor_excursions' AND COLUMN_NAME = 'excursion_id'
            AND REFERENCED_TABLE_NAME = 'excursions';
        """)
        excursion_fk = self.cursor.fetchone()
        self.assertIsNotNone(excursion_fk, "Visitor_excursions table does not have foreign key constraint on 'excursion_id'")

    def test_visitor_excursions_composite_primary_key(self):
        """Test that visitor_excursions table has a composite primary key on visitor_id and excursion_id"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
            WHERE TABLE_NAME = 'visitor_excursions' AND CONSTRAINT_TYPE = 'PRIMARY KEY';
        """)
        primary_key = self.cursor.fetchone()
        self.assertIsNotNone(primary_key, "Visitor_excursions table does not have a primary key")

        self.cursor.execute("""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'visitor_excursions' AND CONSTRAINT_NAME = %s
            ORDER BY ORDINAL_POSITION;
        """, (primary_key[0],))
        primary_key_columns = [column[0] for column in self.cursor.fetchall()]
        # Order might vary depending on creation order, check both columns exist
        self.assertIn('visitor_id', primary_key_columns, "PK missing visitor_id")
        self.assertIn('excursion_id', primary_key_columns, "PK missing excursion_id")
        self.assertEqual(len(primary_key_columns), 2, "PK should have exactly 2 columns")


    def test_visitor_excursions_data_insertion(self):
        """Test data insertion into visitor_excursions table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO visitor_excursions (visitor_id, excursion_id) VALUES (%s, %s)", (self.visitor_id, self.excursion_id))
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM visitor_excursions WHERE visitor_id = %s AND excursion_id = %s", (self.visitor_id, self.excursion_id))
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into visitor_excursions table")

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into visitor_excursions table: {e}")

    def test_visitor_excursions_foreign_key_enforcement(self):
        """Test foreign key constraint enforcement in visitor_excursions table"""
        try:
            # Try inserting invalid data (non-existent visitor_id)
            self.cursor.execute("INSERT INTO visitor_excursions (visitor_id, excursion_id) VALUES (99999, %s)", (self.excursion_id,))
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent visitor_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate visitor_id foreign key constraint violation")

        try:
            # Try inserting invalid data (non-existent excursion_id)
            self.cursor.execute("INSERT INTO visitor_excursions (visitor_id, excursion_id) VALUES (%s, 99999)", (self.visitor_id,))
            self.connection.commit()
            self.fail("Should not allow insertion of data with non-existent excursion_id")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("foreign key constraint fails", str(e).lower(), "Error message does not indicate excursion_id foreign key constraint violation")

if __name__ == '__main__':
    unittest.main()
