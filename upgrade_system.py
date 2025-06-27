from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List

__all__ = [
    "Upgrade",
    "Combo",
    "UpgradeRegistry",
    "combo_from_names",
    "rename_uppercase",
    "add_prefix",
    "add_suffix",
    "change_extension",
]


@dataclass
class Upgrade:
    """Represents an upgrade action applied to a file."""

    name: str
    action: Callable[[Path], Path]

    def apply(self, path: Path) -> Path:
        return self.action(path)


class UpgradeRegistry:
    """Registry for named upgrade actions."""

    def __init__(self) -> None:
        self._registry: Dict[str, Callable[[Path], Path]] = {}

    def register(
        self, name: str
    ) -> Callable[[Callable[[Path], Path]], Callable[[Path], Path]]:
        def decorator(func: Callable[[Path], Path]) -> Callable[[Path], Path]:
            self._registry[name] = func
            return func

        return decorator

    def get(self, name: str) -> Callable[[Path], Path]:
        if name not in self._registry:
            raise KeyError(f"Unknown upgrade: {name}")
        return self._registry[name]

    def create_upgrade(self, name: str) -> Upgrade:
        return Upgrade(name, self.get(name))

    def list(self) -> List[str]:
        return list(self._registry.keys())


registry = UpgradeRegistry()


@dataclass
class Combo:
    """A sequence of upgrades executed together."""

    name: str
    upgrades: Iterable[Upgrade]

    def apply(self, path: Path) -> Path:
        for upgrade in self.upgrades:
            path = upgrade.apply(path)
        return path


def combo_from_names(
    name: str, upgrade_names: Iterable[str], reg: UpgradeRegistry = registry
) -> Combo:
    """Create a :class:`Combo` from registered upgrade names."""

    upgrades = [reg.create_upgrade(u) for u in upgrade_names]
    return Combo(name, upgrades)


@registry.register("rename_uppercase")
def rename_uppercase(path: Path) -> Path:
    """Rename ``path`` to have an uppercase name."""

    new_path = path.with_name(path.name.upper())
    if new_path.exists():
        raise FileExistsError(f"Target file already exists: {new_path}")
    path.rename(new_path)
    return new_path


def add_prefix(prefix: str) -> Callable[[Path], Path]:
    """Return an upgrade that prepends ``prefix`` to the file name."""

    @registry.register(f"add_prefix:{prefix}")
    def _inner(path: Path) -> Path:
        new_path = path.with_name(prefix + path.name)
        if new_path.exists():
            raise FileExistsError(f"Target file already exists: {new_path}")
        path.rename(new_path)
        return new_path

    return _inner


def add_suffix(suffix: str) -> Callable[[Path], Path]:
    """Return an upgrade that appends ``suffix`` before the extension."""

    @registry.register(f"add_suffix:{suffix}")
    def _inner(path: Path) -> Path:
        stem = path.stem + suffix
        new_path = path.with_name(stem + path.suffix)
        if new_path.exists():
            raise FileExistsError(f"Target file already exists: {new_path}")
        path.rename(new_path)
        return new_path

    return _inner


def change_extension(ext: str) -> Callable[[Path], Path]:
    """Return an upgrade that changes the file extension to ``ext``."""

    @registry.register(f"change_extension:{ext}")
    def _inner(path: Path) -> Path:
        new_path = path.with_suffix(ext)
        if new_path.exists():
            raise FileExistsError(f"Target file already exists: {new_path}")
        path.rename(new_path)
        return new_path

    return _inner
