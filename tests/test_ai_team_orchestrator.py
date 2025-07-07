import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from ai_team_orchestrator import AITeamOrchestrator
from config import Config
from database import Database


class DummyConfig(Config):
    def __init__(self):
        pass


class DummyDatabase(Database):
    def __init__(self):
        pass


class TestAITeamOrchestrator(unittest.TestCase):
    def setUp(self):
        self.tmpdir = os.path.abspath("tmp_test")
        os.makedirs(self.tmpdir, exist_ok=True)
        self.files = []
        for i in range(2):
            path = os.path.join(self.tmpdir, f"file{i}.txt")
            with open(path, "w") as f:
                f.write("content")
            self.files.append(path)

    def tearDown(self):
        for f in self.files:
            if os.path.exists(f):
                os.remove(f)
        if os.path.exists(self.tmpdir):
            os.rmdir(self.tmpdir)

    @patch("os.rename")
    def test_orchestrate(self, mock_rename):
        class DummyAnalyzer:
            def __init__(self, laws_file):
                pass

            def analyze_case_file(self, path):
                return {"file": path}

        orchestrator = AITeamOrchestrator(
            DummyConfig(),
            DummyDatabase(),
            "laws.json",
            analyzer_cls=DummyAnalyzer,
            sort_func=lambda p: None,
            rename_func=lambda p: f"renamed_{os.path.basename(p)}",
        )
        orchestrator.optimizer.evolutionary_optimize_file_order = lambda ops: ops
        results = orchestrator.orchestrate(self.files)
        self.assertEqual(len(results), 2)
        self.assertEqual(mock_rename.call_count, 2)


if __name__ == "__main__":
    unittest.main()
