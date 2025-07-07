import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
)  # noqa: E402
from file_summarizer import (
    summarize_files,
    summarize_files_parallel,
    summarize_path,
)  # noqa: E402


class FakeInference:
    def create_completion(self, prompt):
        return {"choices": [{"text": "test summary"}]}


class TestSummarizer(unittest.TestCase):
    def test_summarize_files(self):
        test_file = "sample_test.txt"
        with open(test_file, "w") as f:
            f.write("This is a sample text file. It has two sentences.")

        summaries = summarize_files([test_file], FakeInference())
        self.assertIn(test_file, summaries)
        self.assertEqual(summaries[test_file], "test summary")

        summaries2 = summarize_path(test_file, FakeInference())
        self.assertIn(test_file, summaries2)
        self.assertEqual(summaries2[test_file], "test summary")

        os.remove(test_file)

    def test_summarize_files_parallel(self):
        test_file = "sample_test.txt"
        with open(test_file, "w") as f:
            f.write("This is a sample text file. It has two sentences.")

        summaries = summarize_files_parallel([test_file], FakeInference(), workers=2)
        self.assertIn(test_file, summaries)
        self.assertEqual(summaries[test_file], "test summary")

        os.remove(test_file)

    def test_summarize_path_directory(self):
        test_dir = "sample_dir"
        os.makedirs(test_dir, exist_ok=True)
        file1 = os.path.join(test_dir, "file1.txt")
        file2 = os.path.join(test_dir, "file2.txt")
        with open(file1, "w") as f:
            f.write("Content of file one.")
        with open(file2, "w") as f:
            f.write("Content of file two.")

        summaries = summarize_path(test_dir, FakeInference(), parallel=True, workers=2)
        self.assertIn(file1, summaries)
        self.assertIn(file2, summaries)

        os.remove(file1)
        os.remove(file2)
        os.rmdir(test_dir)

    def test_summarize_path_missing(self):
        with self.assertRaises(FileNotFoundError):
            summarize_path("nonexistent.txt", FakeInference())


if __name__ == "__main__":
    unittest.main()
