from legal_case_manager import LegalCaseManager
from legal_case_pb2 import Case, Document


def test_case_manager_roundtrip(tmp_path):
    manager = LegalCaseManager()
    root_case = Case(id="1", title="Root")
    sub_case = Case(id="1.1", title="Child")
    manager.add_case(root_case)
    manager.add_case(sub_case, parent_id="1")
    doc = Document(id="d1", name="contract", type="pdf")
    manager.add_document("1.1", doc)
    dest = tmp_path / "case.bin"
    manager.to_file(dest)
    new_manager = LegalCaseManager()
    new_manager.load_from_file(dest)
    assert new_manager.org.cases[0].sub_cases[0].documents[0].name == "contract"
