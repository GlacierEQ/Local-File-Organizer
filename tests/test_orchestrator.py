from __future__ import annotations

import json
import tempfile
from pathlib import Path
import unittest
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))  # noqa: E402

from upgrade_system import (  # noqa: E402
    Upgrade,
    Combo,
    rename_uppercase,
    add_prefix,
)
from file_upgrade_orchestrator import (  # noqa: E402
    FileUpgradeOrchestrator,
    CaseLogger,
)


class TestFileUpgradeOrchestrator(unittest.TestCase):
    def test_process_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dir_path = Path(tmpdir)
            (dir_path / "a.txt").write_text("data")
            (dir_path / "b.txt").write_text("data")

            combo = Combo(
                "test",
                [
                    Upgrade("upper", rename_uppercase),
                    Upgrade("pref", add_prefix("x_")),
                ],
            )
            log_file = dir_path / "log.jsonl"
            orchestrator = FileUpgradeOrchestrator(
                combo, CaseLogger(log_file), workers=2, batch_size=1
            )
            result_paths = sorted(orchestrator.process_directory(dir_path))

            self.assertEqual(
                [p.name for p in result_paths],
                ["x_A.TXT", "x_B.TXT"],
            )

            log_content = log_file.read_text().splitlines()
            logs = [json.loads(line) for line in log_content]
            self.assertEqual(len(logs), 2)
            self.assertEqual(
                {log["new_path"] for log in logs},
                {str(dir_path / "x_A.TXT"), str(dir_path / "x_B.TXT")},
            )
            self.assertTrue(all(log["status"] == "success" for log in logs))


if __name__ == "__main__":
    unittest.main()
