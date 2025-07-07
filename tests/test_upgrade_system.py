from pathlib import Path
import tempfile
import unittest
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))  # noqa: E402

from upgrade_system import (  # noqa: E402
    Upgrade,
    Combo,
    combo_from_names,
    rename_uppercase,
    rename_lowercase,
    add_prefix,
)


class TestUpgradeSystem(unittest.TestCase):
    def test_single_upgrade(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "sample.txt"
            file_path.write_text("data")
            upgrade = Upgrade("upper", rename_uppercase)
            new_path = upgrade.apply(file_path)
            self.assertTrue(new_path.exists())
            self.assertEqual(new_path.name, "SAMPLE.TXT")

    def test_combo_upgrade(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "sample.txt"
            file_path.write_text("data")
            upper = Upgrade("upper", rename_uppercase)
            prefix = Upgrade("prefix", add_prefix("new_"))
            combo = Combo("combo1", [upper, prefix])
            new_path = combo.apply(file_path)
            self.assertTrue(new_path.exists())
            self.assertEqual(new_path.name, "new_SAMPLE.TXT")

    def test_lowercase_upgrade(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "Sample.txt"
            file_path.write_text("data")
            upgrade = Upgrade("lower", rename_lowercase)
            new_path = upgrade.apply(file_path)
            self.assertEqual(new_path.name, "sample.txt")

    def test_registry_and_combo_from_names(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "sample.txt"
            file_path.write_text("data")
            combo = combo_from_names(
                "auto",
                [
                    "rename_uppercase",
                    "add_prefix:new_",
                    "add_suffix:_v1",
                    "change_extension:.md",
                ],
            )
            new_path = combo.apply(file_path)
            self.assertTrue(new_path.exists())
            self.assertEqual(new_path.name, "new_SAMPLE_v1.md")

    def test_existing_file_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "sample.txt"
            file_path.write_text("data")
            target = Path(tmpdir) / "SAMPLE.TXT"
            target.write_text("exists")
            upgrade = Upgrade("upper", rename_uppercase)
            with self.assertRaises(FileExistsError):
                upgrade.apply(file_path)


if __name__ == "__main__":
    unittest.main()
