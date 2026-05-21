from __future__ import annotations

from traceguard.domain.coverage import Severity, ValidationFinding
from traceguard.domain.requirement import Requirement
from traceguard.parser.controlled_language import find_vague_terms


def validate_verifiability(requirements: list[Requirement]) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    for requirement in requirements:
        vague = find_vague_terms(requirement.text)
        if vague:
            findings.append(
                ValidationFinding(
                    code="R-VERIF-001",
                    message=f"{requirement.id} contains unverifiable wording: {', '.join(vague)}.",
                    severity=Severity.MEDIUM,
                )
            )
    return findings

