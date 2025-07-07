import os
import sys
import shutil
import unittest

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from forensic_organizer import ForensicOrganizer


class DummyInference:
    def create_completion(self, prompt):
        return {"choices": [{"text": "summary"}]}


def dummy_classifier(_text: str) -> str:
    return "TestCat"


class TestForensicOrganizer(unittest.TestCase):
    def setUp(self):
        self.src = "temp_in"
        os.makedirs(self.src, exist_ok=True)
        with open(os.path.join(self.src, "file.txt"), "w") as f:
            f.write("content")
        self.dest = "temp_out"
        self.org = ForensicOrganizer(self.dest, dummy_classifier, DummyInference())

    def tearDown(self):
        shutil.rmtree(self.src, ignore_errors=True)
        shutil.rmtree(self.dest, ignore_errors=True)

    def test_organize_directory(self):
        summaries = self.org.organize_directory(self.src)
        cat_dir = os.path.join(self.dest, "TestCat")
        self.assertTrue(os.path.isdir(cat_dir))
        self.assertEqual(len(os.listdir(cat_dir)), 1)
        self.assertTrue(all(path.startswith(cat_dir) for path in summaries))


if __name__ == "__main__":
    unittest.main()
