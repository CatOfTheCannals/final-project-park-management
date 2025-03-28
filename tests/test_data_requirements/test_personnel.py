import unittest
import pymysql

class TestPersonnelDataRequirements(unittest.TestCase):
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
        self.created_ids = [] # Track created IDs

    def tearDown(self):
        # Clean up test data created during tests
        if self.created_ids:
            with self.connection.cursor() as cursor:
                ids_format = ','.join(['%s'] * len(self.created_ids))
                # Need to delete from subtype tables first
                cursor.execute(f"DELETE FROM management_personnel WHERE personnel_id IN ({ids_format})", tuple(self.created_ids))
                cursor.execute(f"DELETE FROM surveillance_personnel WHERE personnel_id IN ({ids_format})", tuple(self.created_ids))
                cursor.execute(f"DELETE FROM research_personnel WHERE personnel_id IN ({ids_format})", tuple(self.created_ids))
                cursor.execute(f"DELETE FROM conservation_personnel WHERE personnel_id IN ({ids_format})", tuple(self.created_ids))
                # Then delete from personnel
                cursor.execute(f"DELETE FROM personnel WHERE id IN ({ids_format})", tuple(self.created_ids))
            self.connection.commit()
        self.connection.close()

    def test_personnel_table_exists(self):
        """Test that the personnel table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'personnel';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Personnel table does not exist")

    def test_personnel_has_required_columns(self):
        """Test that personnel table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM personnel LIKE 'DNI';")
        dni_column = self.cursor.fetchone()
        self.assertIsNotNone(dni_column, "Personnel table does not have 'DNI' column")

        self.cursor.execute("SHOW COLUMNS FROM personnel LIKE 'CUIL';")
        cuil_column = self.cursor.fetchone()
        self.assertIsNotNone(cuil_column, "Personnel table does not have 'CUIL' column")

        self.cursor.execute("SHOW COLUMNS FROM personnel LIKE 'name';")
        name_column = self.cursor.fetchone()
        self.assertIsNotNone(name_column, "Personnel table does not have 'name' column")

        self.cursor.execute("SHOW COLUMNS FROM personnel LIKE 'address';")
        address_column = self.cursor.fetchone()
        self.assertIsNotNone(address_column, "Personnel table does not have 'address' column")

        self.cursor.execute("SHOW COLUMNS FROM personnel LIKE 'phone_numbers';")
        phone_numbers_column = self.cursor.fetchone()
        self.assertIsNotNone(phone_numbers_column, "Personnel table does not have 'phone_numbers' column")

        self.cursor.execute("SHOW COLUMNS FROM personnel LIKE 'salary';")
        salary_column = self.cursor.fetchone()
        self.assertIsNotNone(salary_column, "Personnel table does not have 'salary' column")

    def test_personnel_dni_cuil_unique(self):
        """Test that DNI and CUIL are unique"""
        # Insert a personnel record
        self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, salary) VALUES ('TESTP123', 'TESTP20123', 'Test Name', 50000.00)")
        inserted_id_1 = self.cursor.lastrowid
        self.created_ids.append(inserted_id_1)
        self.connection.commit()

        # Try inserting another personnel record with the same DNI
        with self.assertRaises(pymysql.err.IntegrityError):
            self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, salary) VALUES ('TESTP123', 'TESTP21123', 'Another Name', 60000.00)")
            inserted_id_2 = self.cursor.lastrowid # If insert succeeds unexpectedly
            self.created_ids.append(inserted_id_2)
            self.connection.commit() # This commit won't be reached if error is raised
        self.connection.rollback() # Rollback after expected error or unexpected success

        # Try inserting another personnel record with the same CUIL
        with self.assertRaises(pymysql.err.IntegrityError):
            self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, salary) VALUES ('TESTP876', 'TESTP20123', 'Yet Another Name', 70000.00)")
            inserted_id_3 = self.cursor.lastrowid # If insert succeeds unexpectedly
            self.created_ids.append(inserted_id_3)
            self.connection.commit() # This commit won't be reached if error is raised
        self.connection.rollback() # Rollback after expected error or unexpected success


    def test_personnel_data_insertion(self):
        """Test data insertion into personnel table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, salary) VALUES ('TESTP987', 'TESTP22987', 'Valid Name', 80000.00)")
            inserted_id = self.cursor.lastrowid
            self.created_ids.append(inserted_id)
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM personnel WHERE id = %s", (inserted_id,))
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into personnel table")
            self.assertEqual(result['DNI'], 'TESTP987')

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into personnel table: {e}")


    def test_personnel_required_fields_not_null(self):
        """Test that required fields (DNI, CUIL, name) cannot be null"""
        try:
        # Try inserting data with NULL DNI
        with self.assertRaises((pymysql.err.IntegrityError, pymysql.err.OperationalError)):
            self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, salary) VALUES (NULL, 'TESTP234', 'Null DNI Name', 90000.00)")
            inserted_id = self.cursor.lastrowid # If insert succeeds unexpectedly
            self.created_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()

        # Try inserting data with NULL CUIL
        with self.assertRaises((pymysql.err.IntegrityError, pymysql.err.OperationalError)):
            self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, salary) VALUES ('TESTP345', NULL, 'Null CUIL Name', 100000.00)")
            inserted_id = self.cursor.lastrowid
            self.created_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()

        # Try inserting data with NULL name
        with self.assertRaises((pymysql.err.IntegrityError, pymysql.err.OperationalError)):
            self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, salary) VALUES ('TESTP456', 'TESTP245', NULL, 110000.00)")
            inserted_id = self.cursor.lastrowid
            self.created_ids.append(inserted_id)
            self.connection.commit()
        self.connection.rollback()
