import os
import sys
import unittest
import tempfile

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from forensic_organizer import ForensicCaseOrganizer  # noqa: E402


class FakeRenamer:
    def __call__(self, path: str) -> str:
        return "renamed" + os.path.splitext(path)[1]


def fake_categorize(path: str) -> str:
    return "case_files"


class FakeAnalyzer:
    def __init__(self) -> None:
        self.analyzed = []

    def analyze_case_file(self, path: str) -> None:
        self.analyzed.append(path)


class TestForensicCaseOrganizer(unittest.TestCase):
    def test_process_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            incoming = os.path.join(tmp, "incoming")
            os.makedirs(incoming)
            file_path = os.path.join(incoming, "doc.txt")
            with open(file_path, "w") as f:
                f.write("hello")

            analyzer = FakeAnalyzer()
            output_root = os.path.join(tmp, "sorted")
            organizer = ForensicCaseOrganizer(
                output_root, FakeRenamer(), fake_categorize, analyzer
            )

            results = organizer.process_directory(incoming)
            expected_path = os.path.join(output_root, "case_files", "renamed.txt")
            self.assertEqual(results, [expected_path])
            self.assertTrue(os.path.isfile(expected_path))
            self.assertEqual(analyzer.analyzed, [expected_path])


if __name__ == "__main__":
    unittest.main()
