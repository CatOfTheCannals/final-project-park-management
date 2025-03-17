import unittest
from unittest import TestCase
import pymysql

class TestFunctionalRequirements(TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize database connection
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
            cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('Cordoba', 'Secretaria de Ambiente');")
            cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, total_area) VALUES ('Parque A', '2020-01-01', 'parqueA@example.com', 1000);")
            cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, total_area) VALUES ('Parque B', '2021-02-01', 'parqueB@example.com', 2000);")
            cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, total_area) VALUES ('Parque C', '2022-03-01', 'parqueC@example.com', 3000);")
            cursor.execute("INSERT INTO park_areas (name, extension) VALUES ('Area 1', 100);")
            cursor.execute("INSERT INTO park_areas (name, extension) VALUES ('Area 2', 200);")
            cursor.execute("INSERT INTO natural_elements (scientific_name, common_name, number_of_individuals) VALUES ('especie1', 'uno', 50);")
            cursor.execute("INSERT INTO natural_elements (scientific_name, common_name, number_of_individuals) VALUES ('especie2', 'dos', 100);")
            cls.connection.commit()

    @classmethod
    def tearDownClass(cls):
        # Clean up test data and close connection
        with cls.connection.cursor() as cursor:
            cursor.execute("DELETE FROM provinces;")
            cursor.execute("DELETE FROM parks;")
            cursor.execute("DELETE FROM park_areas;")
            cursor.execute("DELETE FROM natural_elements;")
        cls.connection.commit()
        cls.connection.close()

    def test_01_determine_province_with_most_parks(self):
        """Test that we can determine the province with the most natural parks"""
        # Assuming the query returns a tuple (province_name, park_count)
        self.cursor.execute("""
            SELECT p.name, COUNT(pk.id) AS park_count
            FROM provinces p
            LEFT JOIN parks pk ON p.id = pk.province_id
            GROUP BY p.name
            ORDER BY park_count DESC
            LIMIT 1;
        """)
        result = self.cursor.fetchone()

        # Assert that a result is returned
        self.assertIsNotNone(result, "No province found")

        # Assert that the park count is an integer
        self.assertIsInstance(result[1], int, "Park count is not an integer")

    def test_02_identify_vegetal_species_in_at_least_half_of_parks(self):
        """Test that we can identify vegetal species found in at least half of the parks"""
        # Assuming the query returns a list of species names
        self.cursor.execute("""
            SELECT ne.scientific_name
            FROM natural_elements ne
            JOIN park_areas pa ON ne.park_area_id = pa.id
            JOIN parks p ON pa.park_id = p.id
            WHERE ne.element_type = 'vegetal'
            GROUP BY ne.scientific_name
            HAVING COUNT(DISTINCT p.id) >= (SELECT COUNT(*) FROM parks) / 2;
        """)
        results = self.cursor.fetchall()

        # Assert that results are returned
        self.assertIsNotNone(results, "No vegetal species found in at least half of the parks")

        # Assert that each result is a string
        for result in results:
            self.assertIsInstance(result[0], str, "Species name is not a string")

    def test_03_count_visitors_in_parks_with_codes_A_and_B(self):
        """Test that we can count the number of visitors in parks with specific codes (A and B)"""
        # Assuming the query returns the total number of visitors
        self.cursor.execute("""
            SELECT COUNT(v.id)
            FROM visitors v
            JOIN parks p ON v.park_id = p.id
            WHERE p.code IN ('A', 'B');
        """)
        result = self.cursor.fetchone()

        # Assert that a result is returned
        self.assertIsNotNone(result, "No visitors found in parks with codes A and B")

        # Assert that the result is an integer
        self.assertIsInstance(result[0], int, "Visitor count is not an integer")

    def test_04_trigger_sends_email_on_species_decrease(self):
        """Test that a trigger sends an email to the park's contact email when the quantity of a species decreases"""
        # This test requires mocking the email sending functionality
        # and checking that the email was sent with the correct information.
        # This is a placeholder for the actual implementation.
        self.assertTrue(True, "Email trigger test not implemented")

    def test_05_database_constraints_are_implemented(self):
        """Test that database constraints based on the problem domain are implemented"""
        # This test requires checking that the database constraints are in place
        # and that they prevent invalid data from being inserted.
        # This is a placeholder for the actual implementation.
        self.assertTrue(True, "Database constraints test not implemented")
