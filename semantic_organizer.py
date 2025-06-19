from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class SemanticOrganizer:
    """Organize files into a simple semantic hierarchy."""

    DEFAULT_CATEGORIES: Dict[str, List[str]] = {
        "legal": ["court", "law", "motion", "contract"],
        "finance": ["invoice", "payment", "receipt"],
        "personal": ["photo", "diary", "note"],
    }

    def __init__(
        self,
        base_dir: str,
        rules: Dict[str, List[str]] | None = None,
        cross_refs: List[str] | None = None,
    ) -> None:
        self.base_dir = Path(base_dir)
        self.rules = rules or self.DEFAULT_CATEGORIES
        self.cross_refs = [Path(d) for d in cross_refs or []]

    def classify(self, text: str) -> str:
        lowered = text.lower()
        for category, keywords in self.rules.items():
            if any(keyword in lowered for keyword in keywords):
                return category.capitalize()
        return "Uncategorized"

    def determine_destination(self, file_path: str) -> Path:
        mod_time = os.path.getmtime(file_path)
        year = datetime.fromtimestamp(mod_time).strftime("%Y")
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(2048)
        except Exception:
            content = ""
        category = self.classify(content)
        return self.base_dir / category / year / Path(file_path).name

    def _create_cross_refs(self, dest: Path) -> None:
        for ref_dir in self.cross_refs:
            ref_dir.mkdir(parents=True, exist_ok=True)
            link = ref_dir / dest.name
            if not link.exists():
                link.symlink_to(dest)

    def organize_file(self, file_path: str) -> Path:
        destination = self.determine_destination(file_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        Path(file_path).rename(destination)
        self._create_cross_refs(destination)
        return destination
