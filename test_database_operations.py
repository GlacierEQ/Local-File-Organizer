import unittest
from database import Database  # Updated to import Database class

class TestDatabaseOperations(unittest.TestCase):

    def setUp(self):
        """Set up the database connection before each test."""
        self.db = Database()  # Initialize the Database class
        self.db.connect()  # Assuming connect() initializes the database connection

    def tearDown(self):
        """Close the database connection after each test."""
        self.db.close()  # Assuming close() terminates the database connection

    def test_insert_record(self):
        """Test inserting a record into the database."""
        record = {'name': 'Test', 'value': 123}
        result = self.db.insert(record)  # Updated to use insert method from Database
        self.assertTrue(result)  # Assuming insert returns True on success

    def test_fetch_record(self):
        """Test fetching a record from the database."""
        record_id = 1  # Assuming a record with ID 1 exists
        record = self.db.fetch(record_id)  # Updated to use fetch method from Database
        self.assertIsNotNone(record)  # Ensure the record is fetched successfully

    def test_update_record(self):
        """Test updating a record in the database."""
        record_id = 1  # Assuming a record with ID 1 exists
        updated_record = {'name': 'Updated Test', 'value': 456}
        result = self.db.update(record_id, updated_record)  # Updated to use update method from Database
        self.assertTrue(result)  # Assuming update returns True on success

    def test_delete_record(self):
        """Test deleting a record from the database."""
        record_id = 1  # Assuming a record with ID 1 exists
        result = self.db.delete(record_id)  # Updated to use delete method from Database
        self.assertTrue(result)  # Assuming delete returns True on success

if __name__ == '__main__':
    unittest.main()
