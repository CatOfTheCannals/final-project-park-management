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
        cls.cursor = cls.connection.cursor(pymysql.cursors.DictCursor) # Use DictCursor

        # Insert test data - Provinces
        cls.cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('Buenos Aires', 'OPDS') ON DUPLICATE KEY UPDATE name=name;")
        cls.cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('Cordoba', 'Secretaria de Ambiente') ON DUPLICATE KEY UPDATE name=name;")
        cls.cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('Santa Fe', 'Ministerio de Ambiente') ON DUPLICATE KEY UPDATE name=name;")
        cls.connection.commit()
        cls.province_ba_id = cls.cursor.execute("SELECT id FROM provinces WHERE name = 'Buenos Aires';"); cls.province_ba_id = cls.cursor.fetchone()['id']
        cls.province_co_id = cls.cursor.execute("SELECT id FROM provinces WHERE name = 'Cordoba';"); cls.province_co_id = cls.cursor.fetchone()['id']
        cls.province_sf_id = cls.cursor.execute("SELECT id FROM provinces WHERE name = 'Santa Fe';"); cls.province_sf_id = cls.cursor.fetchone()['id']


        # Insert test data - Parks
        cls.cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES ('Parque A', '2020-01-01', 'parqueA@example.com', 'A', 1000) ON DUPLICATE KEY UPDATE name=name;")
        cls.cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES ('Parque B', '2021-02-01', 'parqueB@example.com', 'B', 2000) ON DUPLICATE KEY UPDATE name=name;")
        cls.cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES ('Parque C', '2022-03-01', 'parqueC@example.com', 'C', 3000) ON DUPLICATE KEY UPDATE name=name;") # Shared park
        cls.connection.commit()
        cls.park_a_id = cls.cursor.execute("SELECT id FROM parks WHERE code = 'A';"); cls.park_a_id = cls.cursor.fetchone()['id']
        cls.park_b_id = cls.cursor.execute("SELECT id FROM parks WHERE code = 'B';"); cls.park_b_id = cls.cursor.fetchone()['id']
        cls.park_c_id = cls.cursor.execute("SELECT id FROM parks WHERE code = 'C';"); cls.park_c_id = cls.cursor.fetchone()['id']

        # Insert test data - Park Provinces (Linking parks to provinces)
        cls.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, %s, 1000) ON DUPLICATE KEY UPDATE park_id=park_id;", (cls.park_a_id, cls.province_ba_id))
        cls.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, %s, 2000) ON DUPLICATE KEY UPDATE park_id=park_id;", (cls.park_b_id, cls.province_co_id))
        cls.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, %s, 1500) ON DUPLICATE KEY UPDATE park_id=park_id;", (cls.park_c_id, cls.province_co_id)) # Shared C
        cls.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, %s, 1500) ON DUPLICATE KEY UPDATE park_id=park_id;", (cls.park_c_id, cls.province_sf_id)) # Shared C
        cls.connection.commit()

        # Insert test data - Park Areas
        cls.cursor.execute("INSERT INTO park_areas (park_id, area_number, name, extension) VALUES (%s, 1, 'Area A1', 500) ON DUPLICATE KEY UPDATE name=name;", (cls.park_a_id,))
        cls.cursor.execute("INSERT INTO park_areas (park_id, area_number, name, extension) VALUES (%s, 2, 'Area A2', 500) ON DUPLICATE KEY UPDATE name=name;", (cls.park_a_id,))
        cls.cursor.execute("INSERT INTO park_areas (park_id, area_number, name, extension) VALUES (%s, 1, 'Area B1', 2000) ON DUPLICATE KEY UPDATE name=name;", (cls.park_b_id,))
        cls.cursor.execute("INSERT INTO park_areas (park_id, area_number, name, extension) VALUES (%s, 1, 'Area C1', 1500) ON DUPLICATE KEY UPDATE name=name;", (cls.park_c_id,)) # Area in shared park C
        cls.cursor.execute("INSERT INTO park_areas (park_id, area_number, name, extension) VALUES (%s, 2, 'Area C2', 1500) ON DUPLICATE KEY UPDATE name=name;", (cls.park_c_id,)) # Area in shared park C
        cls.connection.commit()

        # Insert test data - Natural Elements (Species)
        cls.cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('Plantus communis', 'Common Plant') ON DUPLICATE KEY UPDATE scientific_name=scientific_name;")
        cls.cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('Plantus rarus', 'Rare Plant') ON DUPLICATE KEY UPDATE scientific_name=scientific_name;")
        cls.cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('Animalia familiaris', 'Familiar Animal') ON DUPLICATE KEY UPDATE scientific_name=scientific_name;")
        cls.connection.commit()
        cls.plant_common_id = cls.cursor.execute("SELECT id FROM natural_elements WHERE scientific_name = 'Plantus communis';"); cls.plant_common_id = cls.cursor.fetchone()['id']
        cls.plant_rare_id = cls.cursor.execute("SELECT id FROM natural_elements WHERE scientific_name = 'Plantus rarus';"); cls.plant_rare_id = cls.cursor.fetchone()['id']
        cls.animal_id = cls.cursor.execute("SELECT id FROM natural_elements WHERE scientific_name = 'Animalia familiaris';"); cls.animal_id = cls.cursor.fetchone()['id']

        # Insert test data - Vegetal Elements (Link to Natural Elements)
        cls.cursor.execute("INSERT INTO vegetal_elements (element_id, flowering_period) VALUES (%s, 'Spring') ON DUPLICATE KEY UPDATE element_id=element_id;", (cls.plant_common_id,))
        cls.cursor.execute("INSERT INTO vegetal_elements (element_id, flowering_period) VALUES (%s, 'Summer') ON DUPLICATE KEY UPDATE element_id=element_id;", (cls.plant_rare_id,))
        cls.connection.commit()

        # Insert test data - Area Elements (Linking species to areas)
        # Common plant in A1, B1, C1 (3 parks)
        cls.cursor.execute("INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES (%s, 1, %s, 100) ON DUPLICATE KEY UPDATE park_id=park_id;", (cls.park_a_id, cls.plant_common_id))
        cls.cursor.execute("INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES (%s, 1, %s, 50) ON DUPLICATE KEY UPDATE park_id=park_id;", (cls.park_b_id, cls.plant_common_id))
        cls.cursor.execute("INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES (%s, 1, %s, 200) ON DUPLICATE KEY UPDATE park_id=park_id;", (cls.park_c_id, cls.plant_common_id))
        # Rare plant only in A2 (1 park)
        cls.cursor.execute("INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES (%s, 2, %s, 10) ON DUPLICATE KEY UPDATE park_id=park_id;", (cls.park_a_id, cls.plant_rare_id))
        # Animal in C2 (1 park)
        cls.cursor.execute("INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES (%s, 2, %s, 20) ON DUPLICATE KEY UPDATE park_id=park_id;", (cls.park_c_id, cls.animal_id))
        cls.connection.commit()

        # Insert test data - Accommodations
        cls.cursor.execute("INSERT INTO accommodations (capacity, category) VALUES (2, 'Cabin A') ON DUPLICATE KEY UPDATE category=category;")
        cls.cursor.execute("INSERT INTO accommodations (capacity, category) VALUES (4, 'Lodge B') ON DUPLICATE KEY UPDATE category=category;")
        cls.connection.commit()
        cls.accom_a_id = cls.cursor.execute("SELECT id FROM accommodations WHERE category = 'Cabin A';"); cls.accom_a_id = cls.cursor.fetchone()['id']
        cls.accom_b_id = cls.cursor.execute("SELECT id FROM accommodations WHERE category = 'Lodge B';"); cls.accom_b_id = cls.cursor.fetchone()['id']

        # Insert test data - Visitors
        cls.cursor.execute("INSERT INTO visitors (DNI, name, address, profession, accommodation_id, park_id) VALUES ('VISITOR1', 'Visitor One', 'Addr 1', 'Prof 1', %s, %s) ON DUPLICATE KEY UPDATE DNI=DNI;", (cls.accom_a_id, cls.park_a_id)) # Visitor in Park A
        cls.cursor.execute("INSERT INTO visitors (DNI, name, address, profession, accommodation_id, park_id) VALUES ('VISITOR2', 'Visitor Two', 'Addr 2', 'Prof 2', %s, %s) ON DUPLICATE KEY UPDATE DNI=DNI;", (cls.accom_b_id, cls.park_b_id)) # Visitor in Park B
        cls.cursor.execute("INSERT INTO visitors (DNI, name, address, profession, accommodation_id, park_id) VALUES ('VISITOR3', 'Visitor Three', 'Addr 3', 'Prof 3', %s, %s) ON DUPLICATE KEY UPDATE DNI=DNI;", (cls.accom_b_id, cls.park_b_id)) # Visitor in Park B
        cls.cursor.execute("INSERT INTO visitors (DNI, name, address, profession, accommodation_id, park_id) VALUES ('VISITOR4', 'Visitor Four', 'Addr 4', 'Prof 4', %s, %s) ON DUPLICATE KEY UPDATE DNI=DNI;", (cls.accom_a_id, cls.park_c_id)) # Visitor in Park C (using accom A for test)
        cls.connection.commit()


    @classmethod
    def tearDownClass(cls):
        # Clean up test data and close connection - use DELETE and be specific
        with cls.connection.cursor() as cursor:
            cursor.execute("DELETE FROM visitors WHERE DNI LIKE 'VISITOR%';")
            cursor.execute("DELETE FROM accommodations WHERE category IN ('Cabin A', 'Lodge B');")
            cursor.execute("DELETE FROM area_elements WHERE element_id IN (%s, %s, %s);", (cls.plant_common_id, cls.plant_rare_id, cls.animal_id))
            cursor.execute("DELETE FROM vegetal_elements WHERE element_id IN (%s, %s);", (cls.plant_common_id, cls.plant_rare_id))
            cursor.execute("DELETE FROM natural_elements WHERE id IN (%s, %s, %s);", (cls.plant_common_id, cls.plant_rare_id, cls.animal_id))
            cursor.execute("DELETE FROM park_areas WHERE park_id IN (%s, %s, %s);", (cls.park_a_id, cls.park_b_id, cls.park_c_id))
            cursor.execute("DELETE FROM park_provinces WHERE park_id IN (%s, %s, %s);", (cls.park_a_id, cls.park_b_id, cls.park_c_id))
            cursor.execute("DELETE FROM parks WHERE id IN (%s, %s, %s);", (cls.park_a_id, cls.park_b_id, cls.park_c_id))
            cursor.execute("DELETE FROM provinces WHERE id IN (%s, %s, %s);", (cls.province_ba_id, cls.province_co_id, cls.province_sf_id))
        cls.connection.commit()
        cls.connection.close()

    def test_01_determine_province_with_most_parks(self):
        """Test Func Req 1: Determine the province with the most natural parks."""
        # Cordoba should have 2 parks (B and C), BA has 1 (A), SF has 1 (C)
        self.cursor.execute("""
            SELECT p.name, COUNT(pp.park_id) AS park_count
            FROM provinces p
            JOIN park_provinces pp ON p.id = pp.province_id
            GROUP BY p.id, p.name
            ORDER BY park_count DESC
            LIMIT 1;
        """)
        result = self.cursor.fetchone()

        self.assertIsNotNone(result, "Query returned no result")
        self.assertEqual(result['name'], 'Cordoba', "Province with most parks is not Cordoba")
        self.assertEqual(result['park_count'], 2, "Park count for Cordoba should be 2")

    def test_02_identify_vegetal_species_in_at_least_half_of_parks(self):
        """Test Func Req 2: Identify vegetal species found in at least half of the parks."""
        # Total parks = 3. Half = 1.5. Need species in >= 2 parks.
        # Plantus communis is in A, B, C (3 parks). Plantus rarus is only in A (1 park).
        self.cursor.execute("""
            SELECT COUNT(DISTINCT id) as total_parks FROM parks;
        """)
        total_parks = self.cursor.fetchone()['total_parks']
        min_parks_required = (total_parks / 2.0)

        self.cursor.execute("""
            SELECT ne.scientific_name, COUNT(DISTINCT ae.park_id) as park_count
            FROM natural_elements ne
            JOIN vegetal_elements ve ON ne.id = ve.element_id -- Only vegetal
            JOIN area_elements ae ON ne.id = ae.element_id
            GROUP BY ne.id, ne.scientific_name
            HAVING park_count >= %s;
        """, (min_parks_required,))
        results = self.cursor.fetchall()

        self.assertEqual(len(results), 1, "Expected 1 species to be in at least half the parks")
        self.assertEqual(results[0]['scientific_name'], 'Plantus communis', "Expected 'Plantus communis'")
        self.assertGreaterEqual(results[0]['park_count'], min_parks_required, "'Plantus communis' park count is less than required")


    def test_03_count_visitors_in_parks_with_codes_A_and_B(self):
        """Test Func Req 3: Count the number of visitors in parks with specific codes (A and B)."""
        # Park A has 1 visitor. Park B has 2 visitors. Total = 3.
        self.cursor.execute("""
            SELECT COUNT(v.id) as visitor_count
            FROM visitors v
            JOIN parks p ON v.park_id = p.id
            WHERE p.code IN ('A', 'B');
        """)
        result = self.cursor.fetchone()

        self.assertIsNotNone(result, "Query returned no result")
        self.assertEqual(result['visitor_count'], 3, "Expected 3 visitors in parks A and B")
