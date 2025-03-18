import unittest
from unittest import TestCase
import pymysql

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

        # Insert some test data
        with cls.connection.cursor() as cursor:
            cursor.execute("INSERT INTO provinces (name) VALUES ('Buenos Aires');")
            cls.connection.commit()
        
    @classmethod
    def tearDownClass(cls):
        with cls.connection.cursor() as cursor:
            cursor.execute("DELETE FROM provinces WHERE name = 'Buenos Aires';")
        cls.connection.close()

    def test_01_provinces_table_exists(self):
        """Test that the provinces table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'provinces';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Provinces table does not exist")

    def test_02_provinces_has_required_columns(self):
        """Test that provinces table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM provinces LIKE 'name';")
        name_column = self.cursor.fetchone()
        self.assertIsNotNone(name_column, "Provinces table does not have 'name' column")
        
        self.cursor.execute("SHOW COLUMNS FROM provinces LIKE 'responsible_organization';")
        org_column = self.cursor.fetchone()
        self.assertIsNotNone(org_column, "Provinces table does not have 'responsible_organization' column")

    def test_03_provinces_responsible_organization_not_null(self):
        """Test that provinces table enforces NOT NULL constraint on responsible_organization"""
        try:
            # Try inserting a new province with a NULL responsible_organization
            self.cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('New Province', NULL);")
            self.connection.commit()
            self.fail("Should not allow NULL responsible_organization in provinces table")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("cannot be null", str(e).lower(), "Error message does not indicate NULL constraint violation")

    def test_04_parks_table_exists(self):
        """Test that the parks table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'parks';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Parks table does not exist")

    def test_05_parks_has_required_columns(self):
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

    def test_06_park_areas_table_exists(self):
        """Test that the park_areas table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'park_areas';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Park areas table does not exist")

    def test_07_park_areas_has_required_columns(self):
        """Test that park_areas table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM park_areas LIKE 'name';")
        name_column = self.cursor.fetchone()
        self.assertIsNotNone(name_column, "Park areas table does not have 'name' column")

        self.cursor.execute("SHOW COLUMNS FROM park_areas LIKE 'extension';")
        extension_column = self.cursor.fetchone()
        self.assertIsNotNone(extension_column, "Park areas table does not have 'extension' column")

    def test_08_natural_elements_table_exists(self):
        """Test that the natural_elements table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'natural_elements';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Natural elements table does not exist")

    def test_09_natural_elements_has_required_columns(self):
        """Test that natural_elements table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM natural_elements LIKE 'scientific_name';")
        scientific_name_column = self.cursor.fetchone()
        self.assertIsNotNone(scientific_name_column, "Natural elements table does not have 'scientific_name' column")

        self.cursor.execute("SHOW COLUMNS FROM natural_elements LIKE 'common_name';")
        common_name_column = self.cursor.fetchone()
        self.assertIsNotNone(common_name_column, "Natural elements table does not have 'common_name' column")

        self.cursor.execute("SHOW COLUMNS FROM natural_elements LIKE 'number_of_individuals';")
        number_column = self.cursor.fetchone()
        self.assertIsNotNone(number_column, "Natural elements table does not have 'number_of_individuals' column")

    def test_10_vegetal_elements_table_exists(self):
        """Test that the vegetal_elements table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'vegetal_elements';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Vegetal elements table does not exist")

    def test_11_vegetal_elements_has_required_columns(self):
        """Test that vegetal_elements table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM vegetal_elements LIKE 'flowering_period';")
        flowering_period_column = self.cursor.fetchone()
        self.assertIsNotNone(flowering_period_column, "Vegetal elements table does not have 'flowering_period' column")

    def test_12_animal_elements_table_exists(self):
        """Test that the animal_elements table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'animal_elements';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Animal elements table does not exist")

    def test_13_animal_elements_has_required_columns(self):
        """Test that animal_elements table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM animal_elements LIKE 'diet';")
        diet_column = self.cursor.fetchone()
        self.assertIsNotNone(diet_column, "Animal elements table does not have 'diet' column")

        self.cursor.execute("SHOW COLUMNS FROM animal_elements LIKE 'mating_season';")
        mating_season_column = self.cursor.fetchone()
        self.assertIsNotNone(mating_season_column, "Animal elements table does not have 'mating_season' column")

    def test_14_mineral_elements_table_exists(self):
        """Test that the mineral_elements table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'mineral_elements';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Mineral elements table does not exist")

    def test_15_mineral_elements_has_required_columns(self):
        """Test that mineral_elements table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM mineral_elements LIKE 'crystal_or_rock';")
        crystal_or_rock_column = self.cursor.fetchone()
        self.assertIsNotNone(crystal_or_rock_column, "Mineral elements table does not have 'crystal_or_rock' column")

    def test_16_park_personnel_table_exists(self):
        """Test that the park_personnel table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'park_personnel';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Park personnel table does not exist")

    def test_17_park_personnel_has_required_columns(self):
        """Test that park_personnel table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM park_personnel LIKE 'dni';")
        dni_column = self.cursor.fetchone()
        self.assertIsNotNone(dni_column, "Park personnel table does not have 'dni' column")

        self.cursor.execute("SHOW COLUMNS FROM park_personnel LIKE 'cuil';")
        cuil_column = self.cursor.fetchone()
        self.assertIsNotNone(cuil_column, "Park personnel table does not have 'cuil' column")

        self.cursor.execute("SHOW COLUMNS FROM park_personnel LIKE 'name';")
        name_column = self.cursor.fetchone()
        self.assertIsNotNone(name_column, "Park personnel table does not have 'name' column")

        self.cursor.execute("SHOW COLUMNS FROM park_personnel LIKE 'address';")
        address_column = self.cursor.fetchone()
        self.assertIsNotNone(address_column, "Park personnel table does not have 'address' column")

        self.cursor.execute("SHOW COLUMNS FROM park_personnel LIKE 'phone_numbers';")
        phone_numbers_column = self.cursor.fetchone()
        self.assertIsNotNone(phone_numbers_column, "Park personnel table does not have 'phone_numbers' column")

        self.cursor.execute("SHOW COLUMNS FROM park_personnel LIKE 'salary';")
        salary_column = self.cursor.fetchone()
        self.assertIsNotNone(salary_column, "Park personnel table does not have 'salary' column")

        self.cursor.execute("SHOW COLUMNS FROM park_personnel LIKE 'personnel_type';")
        personnel_type_column = self.cursor.fetchone()
        self.assertIsNotNone(personnel_type_column, "Park personnel table does not have 'personnel_type' column")

    def test_18_visitors_table_exists(self):
        """Test that the visitors table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'visitors';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Visitors table does not exist")

    def test_19_visitors_has_required_columns(self):
        """Test that visitors table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM visitors LIKE 'dni';")
        dni_column = self.cursor.fetchone()
        self.assertIsNotNone(dni_column, "Visitors table does not have 'dni' column")

        self.cursor.execute("SHOW COLUMNS FROM visitors LIKE 'name';")
        name_column = self.cursor.fetchone()
        self.assertIsNotNone(name_column, "Visitors table does not have 'name' column")

        self.cursor.execute("SHOW COLUMNS FROM visitors LIKE 'address';")
        address_column = self.cursor.fetchone()
        self.assertIsNotNone(address_column, "Visitors table does not have 'address' column")

        self.cursor.execute("SHOW COLUMNS FROM visitors LIKE 'profession';")
        profession_column = self.cursor.fetchone()
        self.assertIsNotNone(profession_column, "Visitors table does not have 'profession' column")

    def test_20_accommodations_table_exists(self):
        """Test that the accommodations table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'accommodations';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Accommodations table does not exist")

    def test_21_accommodations_has_required_columns(self):
        """Test that accommodations table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM accommodations LIKE 'capacity';")
        capacity_column = self.cursor.fetchone()
        self.assertIsNotNone(capacity_column, "Accommodations table does not have 'capacity' column")

        self.cursor.execute("SHOW COLUMNS FROM accommodations LIKE 'category';")
        category_column = self.cursor.fetchone()
        self.assertIsNotNone(category_column, "Accommodations table does not have 'category' column")

    def test_22_excursions_table_exists(self):
        """Test that the excursions table exists"""
        self.cursor.execute("SHOW TABLES LIKE 'excursions';")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Excursions table does not exist")

    def test_23_excursions_has_required_columns(self):
        """Test that excursions table has required columns"""
        self.cursor.execute("SHOW COLUMNS FROM excursions LIKE 'day_of_week';")
        day_of_week_column = self.cursor.fetchone()
        self.assertIsNotNone(day_of_week_column, "Excursions table does not have 'day_of_week' column")

        self.cursor.execute("SHOW COLUMNS FROM excursions LIKE 'time';")
        time_column = self.cursor.fetchone()
        self.assertIsNotNone(time_column, "Excursions table does not have 'time' column")

    def test_24_required_fields_are_enforced(self):
        """Test that required fields cannot be null"""
        try:
            # Try inserting invalid data into provinces table
            self.cursor.execute("INSERT INTO provinces (name) VALUES (NULL);")
            self.fail("Should not allow NULL name in provinces table")
        except pymysql.err.IntegrityError:
            self.connection.rollback() # Rollback the transaction

    def test_25_data_types_are_enforced(self):
        """Test that correct data types are enforced"""
        try:
            # Try inserting invalid string into numeric field
            self.cursor.execute("INSERT INTO parks (total_area) VALUES ('invalid');")
            self.fail("Should not allow non-numeric value in total_area column")
        except pymysql.err.ProgrammingError:
            self.connection.rollback() # Rollback the transaction
