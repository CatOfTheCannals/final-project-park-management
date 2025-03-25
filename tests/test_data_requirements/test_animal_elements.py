from unittest import TestCase
import pymysql


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
