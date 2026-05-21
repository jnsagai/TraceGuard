from __future__ import annotations

from pathlib import Path

from traceguard.domain.requirement import Requirement


def import_excel_requirements(path: Path) -> list[Requirement]:
    raise NotImplementedError(f"Excel import is planned after the MVP: {path}")

