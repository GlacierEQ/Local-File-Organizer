"""Forensic case file organizer.

This module orchestrates file classification, renaming,
and case analysis to store documents in case-specific
folders. It is designed for extensibility and testability
through dependency injection of classification and
analysis functions.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Callable, List, Optional, TYPE_CHECKING

from smart_filename import generate_smart_filename

if TYPE_CHECKING:  # pragma: no cover - imported for type hints
    from case_analyzer import CaseAnalyzer


class ForensicCaseOrganizer:
    """Coordinate AI-powered sorting and case management."""

    def __init__(
        self,
        incoming_dir: str,
        case_dir: str,
        analyzer: Optional["CaseAnalyzer"] = None,
        classifier: Optional[Callable[[str], str]] = None,
    ) -> None:
        self.incoming_dir = Path(incoming_dir)
        self.case_dir = Path(case_dir)
        if analyzer is None:
            from case_analyzer import CaseAnalyzer

            analyzer = CaseAnalyzer("hawaii_laws.json")
        self.analyzer = analyzer
        if classifier is None:
            from ai_hybrid_classifier import extract_text, classify_document

            def default_classifier(file_path: str) -> str:
                return classify_document(extract_text(file_path))

            self.classifier = default_classifier
        else:
            self.classifier = classifier

    def _determine_case(self, file_path: str) -> str:
        analysis = self.analyzer.analyze_case_file(file_path)
        if analysis and isinstance(analysis, dict):
            return analysis.get("metadata", {}).get("case_number", "unknown_case")
        return "unknown_case"

    def organize(self) -> List[str]:
        """Process all files in the incoming directory."""
        processed: List[str] = []
        for entry in self.incoming_dir.iterdir():
            if not entry.is_file():
                continue
            category = self.classifier(str(entry))
            case_id = self._determine_case(str(entry))
            snippet = entry.stem[:20]
            new_name = generate_smart_filename(entry.name, category, snippet)
            dest = self.case_dir / case_id / category
            dest.mkdir(parents=True, exist_ok=True)
            target = dest / new_name
            shutil.copy2(entry, target)
            processed.append(str(target))
        return processed


def organize_cases(
    incoming_dir: str,
    case_dir: str,
    *,
    analyzer: Optional[CaseAnalyzer] = None,
    classifier: Optional[Callable[[str], str]] = None,
) -> List[str]:
    """Functional wrapper around :class:`ForensicCaseOrganizer`."""
    return ForensicCaseOrganizer(
        incoming_dir, case_dir, analyzer, classifier
    ).organize()
