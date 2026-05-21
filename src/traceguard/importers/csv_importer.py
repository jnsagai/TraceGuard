from __future__ import annotations

import csv
from pathlib import Path

from traceguard.domain.requirement import (
    Requirement,
    RequirementLevel,
    RequirementStatus,
    RequirementType,
)
from traceguard.parser.normalizer import display_clean


def import_csv_requirements(path: Path) -> list[Requirement]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        requirements = []
        for row in reader:
            attrs = {"asil": row.get("asil", "")} if row.get("asil") else {}
            requirements.append(
                Requirement(
                    id=str(row["id"]),
                    level=RequirementLevel(str(row.get("level", "system")).lower()),
                    type=RequirementType(str(row.get("type", "functional")).lower()),
                    text=display_clean(str(row["text"])),
                    source=row.get("source") or str(path),
                    status=RequirementStatus(str(row.get("status", "draft")).lower()),
                    attributes=attrs,
                )
            )
        return requirements

