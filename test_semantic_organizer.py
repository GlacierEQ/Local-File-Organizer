from semantic_organizer import SemanticOrganizer


def test_semantic_organizer(tmp_path):
    organizer = SemanticOrganizer(tmp_path)
    sample = tmp_path / "contract.txt"
    sample.write_text("This contract is subject to law.")
    dest = organizer.organize_file(str(sample))
    assert dest.exists()
    assert dest.parent.parent.name == "Legal"
