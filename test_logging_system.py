import unittest
import logging
from logging.handlers import MemoryHandler

class TestLoggingSystem(unittest.TestCase):

    def setUp(self):
        """Set up a memory handler to capture logs for testing."""
        self.log_handler = MemoryHandler(capacity=10, target=None)
        logging.getLogger().addHandler(self.log_handler)
        logging.getLogger().setLevel(logging.INFO)

    def tearDown(self):
        """Remove the memory handler after each test."""
        logging.getLogger().removeHandler(self.log_handler)

    def test_logging_info(self):
        """Test that info messages are logged correctly."""
        logging.info("This is a test info message.")
        self.assertEqual(len(self.log_handler.buffer), 1)
        self.assertIn("This is a test info message.", self.log_handler.buffer[0].getMessage())

    def test_logging_error(self):
        """Test that error messages are logged correctly."""
        logging.error("This is a test error message.")
        self.assertEqual(len(self.log_handler.buffer), 1)
        self.assertIn("This is a test error message.", self.log_handler.buffer[0].getMessage())

if __name__ == '__main__':
    unittest.main()
