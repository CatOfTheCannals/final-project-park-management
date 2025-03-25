from unittest import TestCase
import pymysql


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

        # Insert some test data
        with cls.connection.cursor() as cursor:
            cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('especie_animal', 'animal');")
            cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('especie_vegetal', 'vegetal');")
            cursor.execute("INSERT INTO natural_elements (scientific_name, common_name) VALUES ('roca', 'mineral');")
            cursor.execute("INSERT INTO vegetal_elements (element_id, flowering_period) VALUES (2, 'spring');")
            cursor.execute("INSERT INTO mineral_elements (element_id, crystal_or_rock) VALUES (3, 'crystal');")
            cls.connection.commit()

        # Get the IDs of the inserted elements
        with cls.connection.cursor() as cursor:
            cursor.execute("SELECT id FROM natural_elements WHERE scientific_name = 'especie_animal';")
            cls.animal_id = cursor.fetchone()['id']
            cursor.execute("SELECT id FROM natural_elements WHERE scientific_name = 'especie_vegetal';")
            cls.vegetal_id = cursor.fetchone()['id']
            cursor.execute("SELECT id FROM natural_elements WHERE scientific_name = 'roca';")
            cls.mineral_id = cursor.fetchone()['id']
            cls.connection.commit()

    @classmethod
    def tearDownClass(cls):
        # Clean up test data
        with cls.connection.cursor() as cursor:
            cursor.execute("DELETE FROM element_food WHERE element_id IN (%s, %s, %s) OR food_element_id IN (%s, %s, %s)", (cls.animal_id, cls.vegetal_id, cls.mineral_id, cls.animal_id, cls.vegetal_id, cls.mineral_id))
            cursor.execute("DELETE FROM vegetal_elements WHERE element_id = %s", (cls.vegetal_id,))
            cursor.execute("DELETE FROM mineral_elements WHERE element_id = %s", (cls.mineral_id,))
            cursor.execute("DELETE FROM natural_elements WHERE id IN (%s, %s, %s)", (cls.animal_id, cls.vegetal_id, cls.mineral_id))
            cls.connection.commit()
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

    def test_element_food_mineral_not_food_constraint(self):
        """Test that the constraint prevents minerals from being listed as food"""
        try:
            # Try inserting data where a mineral is a food source
            self.cursor.execute("INSERT INTO element_food (element_id, food_element_id) VALUES (%s, %s)", (self.animal_id, self.mineral_id))
            self.connection.commit()
            self.fail("Should not allow a mineral to be a food source")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("check_mineral_not_food", str(e).lower(), "Error message does not indicate mineral not food constraint violation")

    def test_element_food_vegetal_not_feeding_constraint(self):
        """Test that the constraint prevents vegetal elements from feeding on other elements"""
        try:
            # Try inserting data where a vegetal element is feeding on another element
            self.cursor.execute("INSERT INTO element_food (element_id, food_element_id) VALUES (%s, %s)", (self.vegetal_id, self.animal_id))
            self.connection.commit()
            self.fail("Should not allow a vegetal element to feed on another element")
        except pymysql.err.IntegrityError as e:
            self.connection.rollback()
            self.assertIn("check_vegetal_not_feeding", str(e).lower(), "Error message does not indicate vegetal not feeding constraint violation")
