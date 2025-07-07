"""Orchestrate forensic-level file sorting, renaming, and case analysis."""

from __future__ import annotations

import os
from typing import Callable, Optional, Any, List


class ForensicCaseOrganizer:
    """Coordinate renaming, sorting and case analysis for incoming files."""

    def __init__(
        self,
        output_root: str,
        renamer: Callable[[str], str],
        categorize: Callable[[str], str],
        case_analyzer: Optional[Any] = None,
    ) -> None:
        self.output_root = output_root
        self.renamer = renamer
        self.categorize = categorize
        self.case_analyzer = case_analyzer
        os.makedirs(self.output_root, exist_ok=True)

    def process_file(self, file_path: str) -> Optional[str]:
        """Rename, categorize, move, and analyze a single file.

        Returns the final path of the organized file or ``None`` if processing
        failed.
        """
        if not os.path.isfile(file_path):
            return None

        dir_name = os.path.dirname(file_path)
        new_name = self.renamer(file_path)
        if not new_name:
            new_name = os.path.basename(file_path)
        renamed_path = os.path.join(dir_name, new_name)
        os.rename(file_path, renamed_path)

        category = self.categorize(renamed_path)
        dest_dir = os.path.join(self.output_root, category)
        os.makedirs(dest_dir, exist_ok=True)
        final_path = os.path.join(dest_dir, os.path.basename(renamed_path))
        os.replace(renamed_path, final_path)

        if self.case_analyzer:
            try:
                self.case_analyzer.analyze_case_file(final_path)
            except Exception:  # pragma: no cover - analysis failures shouldn't crash
                pass
        return final_path

    def process_directory(self, directory: str) -> List[str]:
        """Recursively organize every file in ``directory``."""
        organized: List[str] = []
        for root, _, files in os.walk(directory):
            for name in files:
                path = os.path.join(root, name)
                result = self.process_file(path)
                if result:
                    organized.append(result)
        return organized


__all__ = ["ForensicCaseOrganizer"]
