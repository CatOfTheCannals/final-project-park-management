import unittest
from unittest import TestCase
import pymysql


class TestElementFoodDataRequirements(TestCase):
    # Use setUp and tearDown for test isolation
    def setUp(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='park_management',
            cursorclass=pymysql.cursors.DictCursor # Use DictCursor for consistency
        )
        self.cursor = self.connection.cursor()

        # Insert natural elements and get their IDs
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('test_animal_food', 'animal_food');")
            self.animal_id = cursor.lastrowid
            cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('test_vegetal_food', 'vegetal_food');")
            self.vegetal_id = cursor.lastrowid
            cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('test_mineral_food', 'mineral_food');")
            self.mineral_id = cursor.lastrowid

            # Insert into subtype tables using the obtained IDs
            cursor.execute("INSERT INTO animal_elements (element_id, diet) VALUES (%s, 'omnivore');", (self.animal_id,)) # Need animal subtype for completeness
            cursor.execute("INSERT INTO vegetal_elements (element_id, flowering_period) VALUES (%s, 'spring');", (self.vegetal_id,))
            cursor.execute("INSERT INTO mineral_elements (element_id, crystal_or_rock) VALUES (%s, 'crystal');", (self.mineral_id,))
            self.connection.commit()


    def tearDown(self):
        # Clean up test data - order matters
        with self.connection.cursor() as cursor:
            # Delete from element_food first
            cursor.execute("DELETE FROM element_food WHERE element_id IN (%s, %s, %s) OR food_element_id IN (%s, %s, %s)",
                           (self.animal_id, self.vegetal_id, self.mineral_id, self.animal_id, self.vegetal_id, self.mineral_id))
            # Delete from subtype tables
            cursor.execute("DELETE FROM animal_elements WHERE element_id = %s", (self.animal_id,))
            cursor.execute("DELETE FROM vegetal_elements WHERE element_id = %s", (self.vegetal_id,))
            cursor.execute("DELETE FROM mineral_elements WHERE element_id = %s", (self.mineral_id,))
            # Delete from natural_elements
            cursor.execute("DELETE FROM natural_elements WHERE id IN (%s, %s, %s)",
                           (self.animal_id, self.vegetal_id, self.mineral_id))
            self.connection.commit()
        self.connection.close()

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
        """, (primary_key['CONSTRAINT_NAME'],)) # Access by key for DictCursor
        primary_key_columns = [column['COLUMN_NAME'] for column in self.cursor.fetchall()] # Access by key
        # Order might vary, check presence and count
        self.assertIn('element_id', primary_key_columns, "PK missing element_id")
        self.assertIn('food_element_id', primary_key_columns, "PK missing food_element_id")
        self.assertEqual(len(primary_key_columns), 2, "PK should have exactly 2 columns")


    def test_element_food_mineral_not_food_constraint(self):
        """Test that the trigger prevents minerals from being listed as food"""
        try:
            # Try inserting data where a mineral is a food source
            self.cursor.execute("INSERT INTO element_food (element_id, food_element_id) VALUES (%s, %s)", (self.animal_id, self.mineral_id))
            self.connection.commit()
            self.fail("Should not allow a mineral to be a food source (Trigger failed)")
        except pymysql.err.OperationalError as e: # Trigger SIGNAL raises OperationalError (SQLSTATE 45000)
            self.connection.rollback()
            # Check the specific error message from the trigger
            self.assertIn("minerals cannot be food", str(e).lower(), "Error message does not indicate mineral not food constraint violation")
        except pymysql.err.IntegrityError as e: # Fallback check if SIGNAL behaves differently
             self.connection.rollback()
             self.fail(f"Expected OperationalError due to trigger SIGNAL, but got IntegrityError: {e}")
        except Exception as e:
            self.connection.rollback()
            self.fail(f"An unexpected error occurred: {e}")


    def test_element_food_vegetal_not_feeding_constraint(self):
        """Test that the trigger prevents vegetal elements from feeding on other elements"""
        try:
            # Try inserting data where a vegetal element is feeding on another element
            self.cursor.execute("INSERT INTO element_food (element_id, food_element_id) VALUES (%s, %s)", (self.vegetal_id, self.animal_id))
            self.connection.commit()
            self.fail("Should not allow a vegetal element to feed on another element (Trigger failed)")
        except pymysql.err.OperationalError as e: # Trigger SIGNAL raises OperationalError (SQLSTATE 45000)
            self.connection.rollback()
            # Check the specific error message from the trigger
            self.assertIn("vegetals cannot feed", str(e).lower(), "Error message does not indicate vegetal not feeding constraint violation")
        except pymysql.err.IntegrityError as e: # Fallback check if SIGNAL behaves differently
             self.connection.rollback()
             self.fail(f"Expected OperationalError due to trigger SIGNAL, but got IntegrityError: {e}")
        except Exception as e:
            self.connection.rollback()
            self.fail(f"An unexpected error occurred: {e}")
