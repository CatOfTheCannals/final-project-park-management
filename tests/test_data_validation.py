import unittest
from unittest import TestCase
import pymysql
import csv

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

    def provinces_table_exists(self):
        """Test that the provinces table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'provinces';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Provinces table does not exist")

    def provinces_has_required_columns(self):
        """Test that provinces table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM provinces LIKE 'name';")
        name_column = self.cursor.fetchone()
        self.assertIsNotNone(name_column, "Provinces table does not have 'name' column")

        self.cursor.execute("SHOW COLUMNS FROM provinces LIKE 'responsible_organization';")
        org_column = self.cursor.fetchone()
        self.assertIsNotNone(org_column, "Provinces table does not have 'responsible_organization' column")

    def provinces_responsible_organization_not_null(self):
        """Test that provinces table enforces NOT NULL constraint on responsible_organization"""
        try:
            # Try inserting a new province with a NULL responsible_organization
            self.cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('New Province', NULL);")
            self.connection.commit()
            self.fail("Should not allow NULL responsible_organization in provinces table")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("cannot be null", str(e).lower(), "Error message does not indicate NULL constraint violation")

    def test_provinces_has_unique_responsible_organization(self):
        """Test that each province has one and only one responsible organization"""
        try:
            # Insert a province without a responsible organization
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


class TestParksDataRequirements(TestCase):
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

    def test_parks_table_exists(self):
        """Test that the parks table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'parks';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Parks table does not exist")

    def parks_has_required_columns(self):
        """Test that parks table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM parks LIKE 'name';")
        name_column = self.cursor.fetchone()
        self.assertIsNotNone(name_column, "Parks table does not have 'name' column")

        self.cursor.execute("SHOW COLUMNS FROM parks LIKE 'declaration_date';")
        date_column = self.cursor.fetchone()
        self.assertIsNotNone(date_column, "Parks table does not have 'declaration_date' column")

        self.cursor.execute("SHOW COLUMNS FROM parks LIKE 'contact_email';")
        email_column = self.cursor.fetchone()
        self.assertIsNotNone(email_column, "Parks table does not have 'contact_email' column")

        self.cursor.execute("SHOW COLUMNS FROM parks LIKE 'total_area';")
        area_column = self.cursor.fetchone()
        self.assertIsNotNone(area_column, "Parks table does not have 'total_area' column")


class TestParkAreasDataRequirements(TestCase):
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

    def park_areas_table_exists(self):
        """Test that the park_areas table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'park_areas';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Park areas table does not exist")

    def park_areas_has_required_columns(self):
        """Test that park_areas table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM park_areas LIKE 'name';")
        name_column = self.cursor.fetchone()
        self.assertIsNotNone(name_column, "Park areas table does not have 'name' column")

        self.cursor.execute("SHOW COLUMNS FROM park_areas LIKE 'extension';")
        extension_column = self.cursor.fetchone()
        self.assertIsNotNone(extension_column, "Park areas table does not have 'extension' column")

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

class TestVegetalElementsDataRequirements(TestCase):
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

    def vegetal_elements_table_exists(self):
        """Test that the vegetal_elements table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'vegetal_elements';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Vegetal elements table does not exist")

    def vegetal_elements_has_required_columns(self):
        """Test that vegetal_elements table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM vegetal_elements LIKE 'flowering_period';")
        flowering_period_column = self.cursor.fetchone()
        self.assertIsNotNone(flowering_period_column, "Vegetal elements table does not have 'flowering_period' column")

class TestAnimalElementsDataRequirements(TestCase):
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

    def animal_elements_table_exists(self):
        """Test that the animal_elements table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'animal_elements';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Animal elements table does not exist")

    def animal_elements_has_required_columns(self):
        """Test that animal_elements table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM animal_elements LIKE 'diet';")
        diet_column = self.cursor.fetchone()
        self.assertIsNotNone(diet_column, "Animal elements table does not have 'diet' column")

        self.cursor.execute("SHOW COLUMNS FROM animal_elements LIKE 'mating_season';")
        mating_season_column = self.cursor.fetchone()
        self.assertIsNotNone(mating_season_column, "Animal elements table does not have 'mating_season' column")

class TestMineralElementsDataRequirements(TestCase):
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

    def mineral_elements_table_exists(self):
        """Test that the mineral_elements table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'mineral_elements';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Mineral elements table does not exist")

    def mineral_elements_has_required_columns(self):
        """Test that mineral_elements table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM mineral_elements LIKE 'crystal_or_rock';")
        crystal_or_rock_column = self.cursor.fetchone()
        self.assertIsNotNone(crystal_or_rock_column, "Mineral elements table does not have 'crystal_or_rock' column")

class TestElementFoodDataRequirements(TestCase):
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

    def test_element_food_table_exists(self):
        """Test that the element_food table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'element_food';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Element_food table does not exist")

    def test_element_food_has_required_columns(self):
        """Test that element_food table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM element_food LIKE 'element_id';")
        element_id_column = self.cursor.fetchone()
        self.assertIsNotNone(element_id_column, "Element_food table does not have 'element_id' column")

        self.cursor.execute("SHOW COLUMNS FROM element_food LIKE 'food_element_id';")
        food_element_id_column = self.cursor.fetchone()
        self.assertIsNotNone(food_element_id_column, "Element_food table does not have 'food_element_id' column")

    def test_element_food_foreign_key_constraints(self):
        """Test that element_food table has foreign key constraints"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'element_food' AND COLUMN_NAME = 'element_id'
            AND REFERENCED_TABLE_NAME = 'natural_elements';
        """)
        element_fk = self.cursor.fetchone()
        self.assertIsNotNone(element_fk, "Element_food table does not have foreign key constraint on 'element_id'")

        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'element_food' AND COLUMN_NAME = 'food_element_id'
            AND REFERENCED_TABLE_NAME = 'natural_elements';
        """)
        food_element_fk = self.cursor.fetchone()
        self.assertIsNotNone(food_element_fk, "Element_food table does not have foreign key constraint on 'food_element_id'")

    def test_element_food_composite_primary_key(self):
        """Test that element_food table has a composite primary key on element_id and food_element_id"""
        self.cursor.execute("""
            SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
            WHERE TABLE_NAME = 'element_food' AND CONSTRAINT_TYPE = 'PRIMARY KEY';
        """)
        primary_key = self.cursor.fetchone()
        self.assertIsNotNone(primary_key, "Element_food table does not have a primary key")

        self.cursor.execute("""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'element_food' AND CONSTRAINT_NAME = %s
            ORDER BY ORDINAL_POSITION;
        """, (primary_key[0],))
        primary_key_columns = [column[0] for column in self.cursor.fetchall()]
        self.assertEqual(primary_key_columns, ['element_id', 'food_element_id'], "Element_food table does not have a composite primary key on element_id and food_element_id")

class TestDataValidation(TestCase):
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

    def required_fields_are_enforced(self):
        """Test that required fields cannot be null"""
        try:
            # Try inserting invalid data into provinces table
            self.cursor.execute("INSERT INTO provinces (name) VALUES (NULL);")
            self.fail("Should not allow NULL name in provinces table")
        except pymysql.err.IntegrityError:
            self.connection.rollback() # Rollback the transaction
