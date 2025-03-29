import unittest # Added missing import
from unittest import TestCase
import pymysql

class TestFunctionalRequirements(TestCase):
    # Use setUp and tearDown for test isolation
    def setUp(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='park_management',
            cursorclass=pymysql.cursors.DictCursor # Use DictCursor
        )
        self.cursor = self.connection.cursor()

        # --- Insert test data required for functional tests ---
        # Keep track of created IDs for tearDown
        self.province_ids = []
        self.park_ids = []
        self.element_ids = []
        self.accom_ids = []
        self.visitor_ids = []

        try:
            # Provinces - use unique test names to avoid conflicts with populate_data.sql
            self.cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('Test Buenos Aires', 'OPDS Test');")
            self.province_ids.append(self.cursor.lastrowid)
            self.cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('Test Cordoba', 'Secretaria de Ambiente Test');")
            self.province_ids.append(self.cursor.lastrowid)
            self.cursor.execute("INSERT INTO provinces (name, responsible_organization) VALUES ('Test Santa Fe', 'Ministerio de Ambiente Test');")
            self.province_ids.append(self.cursor.lastrowid)
            self.province_ba_id, self.province_co_id, self.province_sf_id = self.province_ids

            # Parks
            self.cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES ('Parque A', '2020-01-01', 'parqueA@example.com', 'A', 1000);")
            self.park_ids.append(self.cursor.lastrowid)
            self.cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES ('Parque B', '2021-02-01', 'parqueB@example.com', 'B', 2000);")
            self.park_ids.append(self.cursor.lastrowid)
            self.cursor.execute("INSERT INTO parks (name, declaration_date, contact_email, code, total_area) VALUES ('Parque C', '2022-03-01', 'parqueC@example.com', 'C', 3000);") # Shared park
            self.park_ids.append(self.cursor.lastrowid)
            self.park_a_id, self.park_b_id, self.park_c_id = self.park_ids

            # Park Provinces
            self.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, %s, 1000);", (self.park_a_id, self.province_ba_id))
            self.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, %s, 2000);", (self.park_b_id, self.province_co_id))
            self.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, %s, 1500);", (self.park_c_id, self.province_co_id)) # Shared C
            self.cursor.execute("INSERT INTO park_provinces (park_id, province_id, extension_in_province) VALUES (%s, %s, 1500);", (self.park_c_id, self.province_sf_id)) # Shared C

            # Park Areas
            self.cursor.execute("INSERT INTO park_areas (park_id, area_number, name, extension) VALUES (%s, 1, 'Area A1', 500);", (self.park_a_id,))
            self.cursor.execute("INSERT INTO park_areas (park_id, area_number, name, extension) VALUES (%s, 2, 'Area A2', 500);", (self.park_a_id,))
            self.cursor.execute("INSERT INTO park_areas (park_id, area_number, name, extension) VALUES (%s, 1, 'Area B1', 2000);", (self.park_b_id,))
            self.cursor.execute("INSERT INTO park_areas (park_id, area_number, name, extension) VALUES (%s, 1, 'Area C1', 1500);", (self.park_c_id,))
            self.cursor.execute("INSERT INTO park_areas (park_id, area_number, name, extension) VALUES (%s, 2, 'Area C2', 1500);", (self.park_c_id,))

            # Natural Elements (Species)
            self.cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('Plantus communis', 'Common Plant');")
            self.element_ids.append(self.cursor.lastrowid)
            self.cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('Plantus rarus', 'Rare Plant');")
            self.element_ids.append(self.cursor.lastrowid)
            self.cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('Animalia familiaris', 'Familiar Animal');")
            self.element_ids.append(self.cursor.lastrowid)
            self.plant_common_id, self.plant_rare_id, self.animal_id = self.element_ids

            # Vegetal Elements
            self.cursor.execute("INSERT INTO vegetal_elements (element_id, flowering_period) VALUES (%s, 'Spring');", (self.plant_common_id,))
            self.cursor.execute("INSERT INTO vegetal_elements (element_id, flowering_period) VALUES (%s, 'Summer');", (self.plant_rare_id,))

            # Area Elements
            self.cursor.execute("INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES (%s, 1, %s, 100);", (self.park_a_id, self.plant_common_id))
            self.cursor.execute("INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES (%s, 1, %s, 50);", (self.park_b_id, self.plant_common_id))
            self.cursor.execute("INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES (%s, 1, %s, 200);", (self.park_c_id, self.plant_common_id))
            self.cursor.execute("INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES (%s, 2, %s, 10);", (self.park_a_id, self.plant_rare_id))
            self.cursor.execute("INSERT INTO area_elements (park_id, area_number, element_id, number_of_individuals) VALUES (%s, 2, %s, 20);", (self.park_c_id, self.animal_id))

            # Accommodations
            self.cursor.execute("INSERT INTO accommodations (capacity, category) VALUES (2, 'Cabin A');")
            self.accom_ids.append(self.cursor.lastrowid)
            self.cursor.execute("INSERT INTO accommodations (capacity, category) VALUES (4, 'Lodge B');")
            self.accom_ids.append(self.cursor.lastrowid)
            self.accom_a_id, self.accom_b_id = self.accom_ids

            # Visitors
            self.cursor.execute("INSERT INTO visitors (DNI, name, accommodation_id, park_id) VALUES ('VISITOR1', 'Visitor One', %s, %s);", (self.accom_a_id, self.park_a_id))
            self.visitor_ids.append(self.cursor.lastrowid)
            self.cursor.execute("INSERT INTO visitors (DNI, name, accommodation_id, park_id) VALUES ('VISITOR2', 'Visitor Two', %s, %s);", (self.accom_b_id, self.park_b_id))
            self.visitor_ids.append(self.cursor.lastrowid)
            self.cursor.execute("INSERT INTO visitors (DNI, name, accommodation_id, park_id) VALUES ('VISITOR3', 'Visitor Three', %s, %s);", (self.accom_b_id, self.park_b_id))
            self.visitor_ids.append(self.cursor.lastrowid)
            self.cursor.execute("INSERT INTO visitors (DNI, name, accommodation_id, park_id) VALUES ('VISITOR4', 'Visitor Four', %s, %s);", (self.accom_a_id, self.park_c_id))
            self.visitor_ids.append(self.cursor.lastrowid)

            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            # Ensure connection is closed even if setup fails
            self.connection.close()
            raise # Re-raise the exception to fail the test setup


    def tearDown(self):
        # Clean up all test data created in setUp - use DELETE with IN clause for efficiency
        with self.connection.cursor() as cursor:
            if self.visitor_ids:
                ids_format = ','.join(['%s'] * len(self.visitor_ids))
                cursor.execute(f"DELETE FROM visitors WHERE id IN ({ids_format})", tuple(self.visitor_ids))
            if self.accom_ids:
                ids_format = ','.join(['%s'] * len(self.accom_ids))
                cursor.execute(f"DELETE FROM accommodations WHERE id IN ({ids_format})", tuple(self.accom_ids))
            if self.element_ids:
                ids_format = ','.join(['%s'] * len(self.element_ids))
                cursor.execute(f"DELETE FROM area_elements WHERE element_id IN ({ids_format})", tuple(self.element_ids))
                cursor.execute(f"DELETE FROM vegetal_elements WHERE element_id IN ({ids_format})", tuple(self.element_ids))
                # Add deletes for animal/mineral if they were added
                cursor.execute(f"DELETE FROM natural_elements WHERE id IN ({ids_format})", tuple(self.element_ids))
            if self.park_ids:
                ids_format = ','.join(['%s'] * len(self.park_ids))
                cursor.execute(f"DELETE FROM park_areas WHERE park_id IN ({ids_format})", tuple(self.park_ids))
                cursor.execute(f"DELETE FROM park_provinces WHERE park_id IN ({ids_format})", tuple(self.park_ids))
                cursor.execute(f"DELETE FROM parks WHERE id IN ({ids_format})", tuple(self.park_ids))
            if self.province_ids:
                ids_format = ','.join(['%s'] * len(self.province_ids))
                cursor.execute(f"DELETE FROM provinces WHERE id IN ({ids_format})", tuple(self.province_ids))
            # Clear email log specific to trigger test if needed
            cursor.execute("DELETE FROM email_log WHERE element_scientific_name = 'Plantus communis';")

        self.connection.commit()
        self.connection.close()

    def test_01_determine_province_with_most_parks(self):
        """Test Func Req 1: Determine the province with the most natural parks."""
        # Cordoba should have 2 parks (B and C), BA has 1 (A), SF has 1 (C)
        self.cursor.execute("""
            SELECT p.name, COUNT(pp.park_id) AS park_count
            FROM provinces p
            JOIN park_provinces pp ON p.id = pp.province_id
            WHERE p.name LIKE 'Test%'  -- Only consider test provinces
            GROUP BY p.id, p.name
            ORDER BY park_count DESC
            LIMIT 1;
        """)
        result = self.cursor.fetchone()

        self.assertIsNotNone(result, "Query returned no result")
        self.assertEqual(result['name'], 'Test Cordoba', "Province with most parks is not Test Cordoba")
        self.assertEqual(result['park_count'], 2, "Park count for Test Cordoba should be 2")

    def test_02_identify_vegetal_species_in_at_least_half_of_parks(self):
        """Test Func Req 2: Identify vegetal species found in at least half of the parks."""
        # Total parks = 3. Half = 1.5. Need species in >= 2 parks.
        # Plantus communis is in A, B, C (3 parks). Plantus rarus is only in A (1 park).
        self.cursor.execute("""
            SELECT COUNT(DISTINCT id) as total_parks FROM parks WHERE id IN (%s, %s, %s);
        """, (self.park_a_id, self.park_b_id, self.park_c_id))
        total_parks = self.cursor.fetchone()['total_parks']
        min_parks_required = (total_parks / 2.0)

        self.cursor.execute("""
            SELECT ne.scientific_name, COUNT(DISTINCT ae.park_id) as park_count
            FROM natural_elements ne
            JOIN vegetal_elements ve ON ne.id = ve.element_id -- Only vegetal
            JOIN area_elements ae ON ne.id = ae.element_id
            WHERE ae.park_id IN (%s, %s, %s)
            GROUP BY ne.id, ne.scientific_name
            HAVING park_count >= %s;
        """, (self.park_a_id, self.park_b_id, self.park_c_id, min_parks_required))
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

    def test_04_trigger_sends_email_on_species_decrease(self):
        """Test Func Req 4: Trigger logs to email_log when species count decreases."""
        # Use existing test data: Common plant (plant_common_id) in Park A (park_a_id), Area 1
        initial_count = 100
        decreased_count = 90

        # Ensure the initial count is correct (redundant if setup is trusted, but good practice)
        self.cursor.execute("""
            SELECT number_of_individuals FROM area_elements
            WHERE park_id = %s AND area_number = 1 AND element_id = %s;
        """, (self.park_a_id, self.plant_common_id))
        current_record = self.cursor.fetchone()
        self.assertIsNotNone(current_record, "Test data for area_elements not found")
        # If the count isn't the expected initial, update it first without triggering the log check
        if current_record['number_of_individuals'] != initial_count:
             self.cursor.execute("""
                UPDATE area_elements SET number_of_individuals = %s
                WHERE park_id = %s AND area_number = 1 AND element_id = %s;
            """, (initial_count, self.park_a_id, self.plant_common_id))
             self.connection.commit()


        # Clear any previous logs for this specific test case to avoid interference
        self.cursor.execute("DELETE FROM email_log WHERE element_scientific_name = 'Plantus communis' AND park_email = 'parqueA@example.com';")
        self.connection.commit()

        # Perform the update that should trigger the logging
        self.cursor.execute("""
            UPDATE area_elements SET number_of_individuals = %s
            WHERE park_id = %s AND area_number = 1 AND element_id = %s;
        """, (decreased_count, self.park_a_id, self.plant_common_id))
        self.connection.commit()

        # Check if the log entry was created
        self.cursor.execute("""
            SELECT park_email, element_scientific_name, old_count, new_count
            FROM email_log
            WHERE park_email = 'parqueA@example.com' AND element_scientific_name = 'Plantus communis'
            ORDER BY log_timestamp DESC LIMIT 1;
        """)
        log_entry = self.cursor.fetchone()

        self.assertIsNotNone(log_entry, "Trigger did not insert a log entry into email_log")
        self.assertEqual(log_entry['park_email'], 'parqueA@example.com', "Logged park email is incorrect")
        self.assertEqual(log_entry['element_scientific_name'], 'Plantus communis', "Logged element name is incorrect")
        self.assertEqual(log_entry['old_count'], initial_count, "Logged old_count is incorrect")
        self.assertEqual(log_entry['new_count'], decreased_count, "Logged new_count is incorrect")

        # Clean up the log entry created by this test
        self.cursor.execute("DELETE FROM email_log WHERE element_scientific_name = 'Plantus communis' AND park_email = 'parqueA@example.com';")
        self.connection.commit()

    def test_05_species_in_all_parks(self):
        """Test Additional Req 3: Identify species found in all parks."""
        # Setup: Plantus communis is in A, B, C (all 3 parks).
        # Plantus rarus is only in A. Animalia familiaris is only in C.
        self.cursor.execute("SELECT COUNT(DISTINCT id) FROM parks WHERE id IN (%s, %s, %s);", 
                           (self.park_a_id, self.park_b_id, self.park_c_id))
        total_parks = self.cursor.fetchone()['COUNT(DISTINCT id)']

        self.cursor.execute("""
            SELECT ne.scientific_name
            FROM natural_elements ne
            JOIN area_elements ae ON ne.id = ae.element_id
            WHERE ae.park_id IN (%s, %s, %s)
            GROUP BY ne.id, ne.scientific_name
            HAVING COUNT(DISTINCT ae.park_id) = %s;
        """, (self.park_a_id, self.park_b_id, self.park_c_id, total_parks))
        results = self.cursor.fetchall()

        self.assertEqual(len(results), 1, "Expected exactly one species to be in all parks")
        self.assertEqual(results[0]['scientific_name'], 'Plantus communis', "Expected 'Plantus communis' to be in all parks")

    def test_06_species_in_only_one_park(self):
        """Test Additional Req 4: Identify species found in only one park."""
        # Setup: Plantus rarus is only in A. Animalia familiaris is only in C.
        # Plantus communis is in A, B, C.
        self.cursor.execute("""
            SELECT ne.scientific_name, COUNT(DISTINCT ae.park_id) as park_count
            FROM natural_elements ne
            JOIN area_elements ae ON ne.id = ae.element_id
            WHERE ae.park_id IN (%s, %s, %s)
            GROUP BY ne.id, ne.scientific_name
            HAVING park_count = 1;
        """, (self.park_a_id, self.park_b_id, self.park_c_id))
        results = self.cursor.fetchall()
        species_in_one_park = {row['scientific_name'] for row in results}

        self.assertEqual(len(species_in_one_park), 2, "Expected exactly two species to be in only one park")
        self.assertIn('Plantus rarus', species_in_one_park, "Expected 'Plantus rarus' to be in only one park")
        self.assertIn('Animalia familiaris', species_in_one_park, "Expected 'Animalia familiaris' to be in only one park")


        # Clean up: Restore original count (optional, depends if other tests rely on it)
        # self.cursor.execute("""
        #     UPDATE area_elements SET number_of_individuals = %s
        #     WHERE park_id = %s AND area_number = 1 AND element_id = %s;
        # """, (initial_count, self.park_a_id, self.plant_common_id))
        # self.connection.commit()
        # Clean up the log entry created by this test
        self.cursor.execute("DELETE FROM email_log WHERE element_scientific_name = 'Plantus communis' AND park_email = 'parqueA@example.com';")
        self.connection.commit()
