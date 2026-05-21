from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from traceguard.domain.coverage import Severity, ValidationFinding
from traceguard.domain.requirement import Requirement
from traceguard.domain.trace import TraceLink


def load_trace_links(paths: list[Path]) -> list[TraceLink]:
    links: list[TraceLink] = []
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for raw in data.get("links", []):
            links.append(TraceLink.model_validate(raw))
    return links


def validate_trace_links(
    requirements: list[Requirement],
    links: list[TraceLink],
) -> list[ValidationFinding]:
    req_ids = {requirement.id for requirement in requirements}
    atom_ids = {atom.id for requirement in requirements for atom in requirement.atoms}
    findings: list[ValidationFinding] = []
    for link in links:
        if link.source_id not in req_ids:
            findings.append(
                ValidationFinding(
                    code="UNKNOWN_REQUIREMENT_ID",
                    message=f"Trace link references unknown source requirement {link.source_id}.",
                    severity=Severity.HIGH,
                )
            )
        if link.target_id not in req_ids:
            findings.append(
                ValidationFinding(
                    code="UNKNOWN_REQUIREMENT_ID",
                    message=f"Trace link references unknown target requirement {link.target_id}.",
                    severity=Severity.HIGH,
                )
            )
        for atom_id in link.covered_atom_ids:
            if atom_id not in atom_ids:
                findings.append(
                    ValidationFinding(
                        code="UNKNOWN_ATOM_ID",
                        message=f"Trace link references unknown atom {atom_id}.",
                        severity=Severity.HIGH,
                    )
                )
        if link.covered_atom_ids and not link.rationale:
            findings.append(
                ValidationFinding(
                    code="RATIONALE_REQUIRED",
                    message=(
                        f"Trace {link.source_id}->{link.target_id} covers atoms "
                        "without rationale."
                    ),
                    severity=Severity.MEDIUM,
                )
            )
    return findings


def validation_error_to_findings(exc: ValidationError) -> list[ValidationFinding]:
    return [
        ValidationFinding(
            code="SCHEMA_ERROR",
            message=str(error["msg"]),
            severity=Severity.HIGH,
        )
        for error in exc.errors()
    ]
