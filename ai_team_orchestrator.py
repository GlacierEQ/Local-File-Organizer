"""AI Team Orchestrator
======================

Coordinates smart file renaming, sorting, and case analysis. Operations are
optimized to minimize disk thrashing using the evolutionary optimizer from
:mod:`performance`.
"""

from __future__ import annotations

import os
from typing import List, Dict, Optional

from performance import PerformanceOptimizer
from config import Config
from database import Database


class AITeamOrchestrator:
    """Coordinate advanced file processing tasks."""

    def __init__(
        self,
        config: Config,
        database: Database,
        laws_file: str,
        analyzer_cls=None,
        sort_func=None,
        rename_func=None,
    ) -> None:
        self.optimizer = PerformanceOptimizer(config, database)
        # Import heavy modules lazily only if defaults are used
        if analyzer_cls is None:
            from case_analyzer import CaseAnalyzer as analyzer_cls
        if sort_func is None:
            from file_sorter import sort_and_categorize as sort_func
        if rename_func is None:
            from smart_rename import smart_rename_file as rename_func

        self.analyzer = analyzer_cls(laws_file)
        self.sort_func = sort_func
        self.rename_func = rename_func

    def build_rename_operations(self, files: List[str]) -> List[Dict[str, str]]:
        """Create rename operations based on file content."""
        operations: List[Dict[str, str]] = []
        for path in files:
            new_name = self.rename_func(path)
            if new_name:
                dest = os.path.join(os.path.dirname(path), new_name)
                operations.append({"source": path, "destination": dest})
        return operations

    def optimize_operations(
        self, operations: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        if not operations:
            return []
        return self.optimizer.evolutionary_optimize_file_order(operations)

    def execute_renames(self, operations: List[Dict[str, str]]) -> List[str]:
        updated_paths = []
        for op in operations:
            os.rename(op["source"], op["destination"])
            updated_paths.append(op["destination"])
        return updated_paths

    def sort_files(self, files: List[str]) -> None:
        for path in files:
            self.sort_func(path)

    def analyze_cases(self, files: List[str]) -> List[Optional[dict]]:
        return [self.analyzer.analyze_case_file(p) for p in files]

    def orchestrate(self, files: List[str]) -> List[Optional[dict]]:
        renames = self.build_rename_operations(files)
        optimized = self.optimize_operations(renames)
        updated_paths = self.execute_renames(optimized)
        self.sort_files(updated_paths)
        return self.analyze_cases(updated_paths)
