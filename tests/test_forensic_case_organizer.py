from pathlib import Path
from forensic_case_organizer import ForensicCaseOrganizer


class DummyAnalyzer:
    def __init__(self):
        self.files = []

    def analyze_case_file(self, file_path):
        self.files.append(file_path)
        return {"metadata": {"case_number": "CASE123"}}


def dummy_classifier(_path: str) -> str:
    return "Legal"


def test_forensic_case_organizer(tmp_path):
    incoming = tmp_path / "incoming"
    cases = tmp_path / "cases"
    incoming.mkdir()
    cases.mkdir()
    sample = incoming / "doc.txt"
    sample.write_text("hello")

    organizer = ForensicCaseOrganizer(
        str(incoming), str(cases), analyzer=DummyAnalyzer(), classifier=dummy_classifier
    )
    results = organizer.organize()

    assert len(results) == 1
    target = Path(results[0])
    assert target.exists()
    assert target.parent.parent.name == "CASE123"
    assert target.parent.name == "Legal"
