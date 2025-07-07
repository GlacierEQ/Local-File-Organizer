from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
import json

from upgrade_system import Combo


@dataclass
class CaseLogEntry:
    """Record of a single file upgrade operation."""

    timestamp: str
    original_path: str
    new_path: str
    operations: List[str]
    status: str
    error: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self))


class CaseLogger:
    """Append logs of file upgrades to a JSON lines file."""

    def __init__(self, log_file: Path) -> None:
        self.log_file = log_file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, entry: CaseLogEntry) -> None:
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(entry.to_json() + "\n")


class FileUpgradeOrchestrator:
    """Apply combos to all files in a directory with concurrent workers."""

    def __init__(
        self,
        combo: Combo,
        logger: CaseLogger,
        workers: int = 4,
        batch_size: int = 50,
    ) -> None:
        self.combo = combo
        self.logger = logger
        self.workers = workers
        self.batch_size = batch_size

    def process_directory(self, directory: Path) -> List[Path]:
        files = [p for p in directory.iterdir() if p.is_file()]
        results: List[Path] = []
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            for i in range(0, len(files), self.batch_size):
                batch = files[i : i + self.batch_size]  # noqa: E203
                for new_path in executor.map(self._process_file, batch):
                    results.append(new_path)
        return results

    def _process_file(self, path: Path) -> Path:
        original = str(path)
        timestamp = datetime.now(timezone.utc).isoformat()
        try:
            new_path = self.combo.apply(path)
            entry = CaseLogEntry(
                timestamp=timestamp,
                original_path=original,
                new_path=str(new_path),
                operations=[u.name for u in self.combo.upgrades],
                status="success",
            )
            self.logger.log(entry)
            return new_path
        except Exception as exc:  # pragma: no cover - defensive
            entry = CaseLogEntry(
                timestamp=timestamp,
                original_path=original,
                new_path=original,
                operations=[u.name for u in self.combo.upgrades],
                status="error",
                error=str(exc),
            )
            self.logger.log(entry)
            return path
