from __future__ import annotations

import json
from pathlib import Path

from traceguard.domain.coverage import CoverageResult, ValidationFinding


def evidence_payload(
    project: str,
    baseline: str | None,
    results: list[CoverageResult],
    findings: list[ValidationFinding],
) -> dict[str, object]:
    return {
        "project": project,
        "baseline": baseline,
        "results": [result.model_dump(mode="json") for result in sorted(results, key=_result_key)],
        "findings": [finding.model_dump(mode="json") for finding in findings],
    }


def write_evidence_json(
    path: Path,
    project: str,
    baseline: str | None,
    results: list[CoverageResult],
    findings: list[ValidationFinding],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = evidence_payload(project, baseline, results, findings)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _result_key(result: CoverageResult) -> tuple[str, str, str]:
    return (result.parent_requirement_id, result.parent_atom_id, result.rule_id)

