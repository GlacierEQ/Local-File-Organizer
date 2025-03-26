import unittest
from error_handler import handle_error  # Assuming handle_error is the function to be tested

class TestErrorHandling(unittest.TestCase):

    def test_handle_error_logging(self):
        """Test that errors are logged correctly."""
        with self.assertLogs('error_handler', level='ERROR') as log:
            handle_error("Test error message")
            self.assertIn("Test error message", log.output[0])

    def test_handle_error_exceptions(self):
        """Test that exceptions are raised correctly."""
        with self.assertRaises(ValueError):
            handle_error("This should raise an exception")

if __name__ == '__main__':
    unittest.main()
