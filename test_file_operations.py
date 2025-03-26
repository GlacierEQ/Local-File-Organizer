import unittest
import os
from file_utils import collect_file_paths, sanitize_filename  # Assuming these are the functions to be tested

class TestFileOperations(unittest.TestCase):

    def test_collect_file_paths(self):
        """Test collecting file paths from a directory."""
        test_dir = 'test_directory'  # Create a test directory with known files
        os.makedirs(test_dir, exist_ok=True)
        with open(os.path.join(test_dir, 'test_file.txt'), 'w') as f:
            f.write("This is a test file.")

        file_paths = collect_file_paths(test_dir)
        self.assertIn(os.path.join(test_dir, 'test_file.txt'), file_paths)

        # Clean up
        os.remove(os.path.join(test_dir, 'test_file.txt'))
        os.rmdir(test_dir)

    def test_sanitize_filename(self):
        """Test sanitizing a filename."""
        original_name = "Invalid/Name:With*Special?Chars.txt"
        sanitized_name = sanitize_filename(original_name)
        self.assertEqual(sanitized_name, "Invalid_Name_With_Special_Chars.txt")  # Expected sanitized name

if __name__ == '__main__':
    unittest.main()
