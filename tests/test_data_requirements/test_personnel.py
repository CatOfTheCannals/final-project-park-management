import unittest
import pymysql

class TestPersonnelDataRequirements(unittest.TestCase):
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
        # Clean up test data (if any)
        with cls.connection.cursor() as cursor:
            cursor.execute("DELETE FROM personnel WHERE DNI LIKE 'TEST%';")
        cls.connection.commit()
        cls.connection.close()

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
        try:
            # Insert a personnel record
            self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, address, phone_numbers, salary) VALUES ('TEST12345678', 'TEST20123456789', 'Test Name', 'Test Address', '123-456-7890', 50000.00)")
            self.connection.commit()

            # Try inserting another personnel record with the same DNI
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, address, phone_numbers, salary) VALUES ('TEST12345678', 'TEST21123456789', 'Another Test Name', 'Another Test Address', '987-654-3210', 60000.00)")
                self.connection.commit()
            self.connection.rollback()

            # Try inserting another personnel record with the same CUIL
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, address, phone_numbers, salary) VALUES ('TEST87654321', 'TEST20123456789', 'Yet Another Test Name', 'Yet Another Test Address', '555-123-4567', 70000.00)")
                self.connection.commit()
            self.connection.rollback()

        finally:
            # Clean up the test data
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM personnel WHERE DNI LIKE 'TEST%';")
            self.connection.commit()

    def test_personnel_data_insertion(self):
        """Test data insertion into personnel table"""
        try:
            # Insert valid data
            self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, address, phone_numbers, salary) VALUES ('TEST98765432', 'TEST22987654321', 'Valid Name', 'Valid Address', '111-222-3333', 80000.00)")
            self.connection.commit()

            # Verify that the data was inserted
            self.cursor.execute("SELECT * FROM personnel WHERE DNI = 'TEST98765432'")
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "Data was not inserted into personnel table")

        except Exception as e:
            self.connection.rollback()
            self.fail(f"Error inserting data into personnel table: {e}")

        finally:
            # Clean up the test data
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM personnel WHERE DNI LIKE 'TEST%';")
            self.connection.commit()

    def test_personnel_required_fields_not_null(self):
        """Test that required fields (DNI, CUIL, name) cannot be null"""
        try:
            # Try inserting data with NULL DNI
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, address, phone_numbers, salary) VALUES (NULL, 'TEST23456789012', 'Null DNI Name', 'Null DNI Address', '444-555-6666', 90000.00)")
                self.connection.commit()
            self.connection.rollback()

            # Try inserting data with NULL CUIL
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, address, phone_numbers, salary) VALUES ('TEST34567890', NULL, 'Null CUIL Name', 'Null CUIL Address', '555-666-7777', 100000.00)")
                self.connection.commit()
            self.connection.rollback()

            # Try inserting data with NULL name
            with self.assertRaises(pymysql.err.IntegrityError):
                self.cursor.execute("INSERT INTO personnel (DNI, CUIL, name, address, phone_numbers, salary) VALUES ('TEST45678901', 'TEST24567890123', NULL, 'Null Name Address', '666-777-8888', 110000.00)")
                self.connection.commit()
            self.connection.rollback()

        finally:
            # Clean up the test data
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM personnel WHERE DNI LIKE 'TEST%';")
            self.connection.commit()
