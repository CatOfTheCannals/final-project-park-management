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
        
    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def test_03_required_fields_are_enforced(self):
        """Test that required fields cannot be null"""
        with self.connection.cursor() as cursor:
            try:
                # Try inserting invalid data into provinces table
                cursor.execute("INSERT INTO provinces (name) VALUES (NULL);")
                self.fail("Should not allow NULL name in provinces table")
            except pymysql.err.IntegrityError:
                pass
                
    def test_04_data_types_are_enforced(self):
        """Test that correct data types are enforced"""
        with self.connection.cursor() as cursor:
            try:
                # Try inserting invalid string into numeric field
                cursor.execute("INSERT INTO parks (total_area) VALUES ('invalid');")
                self.fail("Should not allow non-numeric value in total_area column") 
            except pymysql.err.ProgrammingError:
                pass
