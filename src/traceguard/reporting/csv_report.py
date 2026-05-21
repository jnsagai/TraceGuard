from __future__ import annotations

import csv
from pathlib import Path

from traceguard.domain.coverage import CoverageResult


def write_csv_report(path: Path, results: list[CoverageResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "parent_id",
                "parent_atom_id",
                "status",
                "child_ids",
                "child_atom_ids",
                "rule_id",
                "severity",
                "explanation",
                "recommended_action",
            ],
        )
        writer.writeheader()
        for result in sorted(results, key=lambda r: (r.parent_requirement_id, r.parent_atom_id)):
            writer.writerow(
                {
                    "parent_id": result.parent_requirement_id,
                    "parent_atom_id": result.parent_atom_id,
                    "status": result.status.value,
                    "child_ids": ";".join(result.child_requirement_ids),
                    "child_atom_ids": ";".join(result.child_atom_ids),
                    "rule_id": result.rule_id,
                    "severity": result.severity.value,
                    "explanation": result.explanation,
                    "recommended_action": result.recommended_action or "",
                }
            )

