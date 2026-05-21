from __future__ import annotations

from pathlib import Path

from traceguard.domain.requirement import Requirement


def import_reqif_requirements(path: Path) -> list[Requirement]:
    raise NotImplementedError(f"ReqIF import is planned after the MVP: {path}")

