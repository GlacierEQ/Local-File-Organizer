from __future__ import annotations

from pathlib import Path

from legal_case_pb2 import Case, Document, LegalOrganization


class LegalCaseManager:
    """Manage hierarchical legal cases using Protocol Buffers."""

    def __init__(self) -> None:
        self.org = LegalOrganization()

    def _find_case(self, cases: list[Case], case_id: str) -> Case | None:
        for case in cases:
            if case.id == case_id:
                return case
            found = self._find_case(list(case.sub_cases), case_id)
            if found:
                return found
        return None

    def add_case(self, case: Case, parent_id: str | None = None) -> None:
        if parent_id is None:
            self.org.cases.append(case)
        else:
            parent = self._find_case(list(self.org.cases), parent_id)
            if parent is None:
                raise ValueError(f"Parent case {parent_id} not found")
            parent.sub_cases.append(case)

    def add_document(self, case_id: str, document: Document) -> None:
        case = self._find_case(list(self.org.cases), case_id)
        if case is None:
            raise ValueError(f"Case {case_id} not found")
        case.documents.append(document)

    def to_file(self, path: str) -> None:
        Path(path).write_bytes(self.org.SerializeToString())

    def load_from_file(self, path: str) -> None:
# import os
# import pathlib

def load_from_file(self, path: str) -> None:
    safe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
    if safe_path.startswith(os.path.dirname(__file__)):
        self.org.ParseFromString(pathlib.Path(safe_path).read_bytes())
    else:
        raise ValueError("Invalid file path")
