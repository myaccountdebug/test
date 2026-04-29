import sys
import sqlite3
from pathlib import Path
import unittest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db import sqlite as db_module

class TestSqlite(unittest.TestCase):
    """Comprehensive test suite for sqlite.py"""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        self.test_db_path = Path(__file__).parent.parent / "db" / "test_fruits.db"
        # Override the DB_PATH for testing
        db_module.DB_PATH = self.test_db_path
        db_module.init_database()
    
    def tearDown(self):
        """Clean up after each test."""
        if self.test_db_path.exists():
            self.test_db_path.unlink()
    
    def test_init_database(self):
        """Test that database and table are created properly."""
        self.assertTrue(self.test_db_path.exists(), "Database file should exist")
        
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='fruits'")
        table = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(table, "fruits table should exist")
    
    def test_insert_single_fruit(self):
        """Test inserting a single fruit."""
        result = db_module.insert_fruit("Apple")
        self.assertTrue(result, "insert_fruit should return True for valid input")
        
        fruits = db_module.get_all_fruits()
        self.assertEqual(len(fruits), 1, "Should have 1 fruit in database")
        self.assertEqual(fruits[0][1], "Apple", "Fruit name should be Apple")
    
    def test_insert_duplicate_fruit(self):
        """Test that duplicate fruits are rejected."""
        db_module.insert_fruit("Banana")
        result = db_module.insert_fruit("Banana")
        
        self.assertFalse(result, "Inserting duplicate should return False")
        
        fruits = db_module.get_all_fruits()
        self.assertEqual(len(fruits), 1, "Should still have only 1 fruit")
    
    def test_insert_multiple_fruits(self):
        """Test inserting multiple fruits."""
        fruit_list = ["Apple", "Banana", "Orange", "Mango"]
        results = db_module.insert_fruits(fruit_list)
        
        self.assertEqual(len(results), 4, "Should return 4 results")
        self.assertTrue(all(result[1] for result in results), "All should be successful")
        
        fruits = db_module.get_all_fruits()
        self.assertEqual(len(fruits), 4, "Should have 4 fruits in database")
    
    def test_insert_multiple_with_duplicate(self):
        """Test inserting multiple fruits with a duplicate."""
        fruit_list = ["Apple", "Banana", "Apple", "Orange"]
        results = db_module.insert_fruits(fruit_list)
        
        self.assertEqual(len(results), 4, "Should return 4 results")
        self.assertTrue(results[0][1], "First Apple should succeed")
        self.assertFalse(results[2][1], "Second Apple should fail")
        
        fruits = db_module.get_all_fruits()
        self.assertEqual(len(fruits), 3, "Should have 3 unique fruits")
    
    def test_get_all_fruits_empty(self):
        """Test getting fruits from an empty database."""
        fruits = db_module.get_all_fruits()
        self.assertEqual(len(fruits), 0, "Empty database should return empty list")
    
    def test_get_all_fruits_ordered(self):
        """Test that fruits are returned in insertion order."""
        db_module.insert_fruit("Zebra Apple")
        db_module.insert_fruit("Apple")
        db_module.insert_fruit("Mango")
        
        fruits = db_module.get_all_fruits()
        self.assertEqual(fruits[0][1], "Zebra Apple", "First inserted should be first")
        self.assertEqual(fruits[1][1], "Apple", "Second inserted should be second")
        self.assertEqual(fruits[2][1], "Mango", "Third inserted should be third")
    
    def test_delete_fruit(self):
        """Test deleting a fruit."""
        db_module.insert_fruit("Apple")
        db_module.insert_fruit("Banana")
        
        result = db_module.delete_fruit("Apple")
        self.assertTrue(result, "delete_fruit should return True")
        
        fruits = db_module.get_all_fruits()
        self.assertEqual(len(fruits), 1, "Should have 1 fruit left")
        self.assertEqual(fruits[0][1], "Banana", "Remaining fruit should be Banana")
    
    def test_delete_nonexistent_fruit(self):
        """Test deleting a fruit that doesn't exist."""
        result = db_module.delete_fruit("NonExistent")
        self.assertFalse(result, "delete_fruit should return False for nonexistent fruit")
    
    def test_clear_all_fruits(self):
        """Test clearing all fruits."""
        db_module.insert_fruits(["Apple", "Banana", "Orange"])
        db_module.clear_all_fruits()
        
        fruits = db_module.get_all_fruits()
        self.assertEqual(len(fruits), 0, "Database should be empty after clear_all_fruits")
    
    def test_fruit_data_structure(self):
        """Test that fruit data has correct structure (id, name, created_at)."""
        db_module.insert_fruit("Apple")
        fruits = db_module.get_all_fruits()
        
        self.assertEqual(len(fruits[0]), 3, "Each fruit should have 3 fields")
        self.assertIsInstance(fruits[0][0], int, "ID should be integer")
        self.assertIsInstance(fruits[0][1], str, "Name should be string")
        self.assertIsInstance(fruits[0][2], str, "created_at should be string")
    
    def test_case_sensitivity_in_names(self):
        """Test that fruit names are case-sensitive."""
        db_module.insert_fruit("apple")
        result = db_module.insert_fruit("Apple")
        
        self.assertTrue(result, "apple and Apple should be different")
        fruits = db_module.get_all_fruits()
        self.assertEqual(len(fruits), 2, "Should have 2 fruits")

if __name__ == '__main__':
    unittest.main()