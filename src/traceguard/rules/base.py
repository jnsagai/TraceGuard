from __future__ import annotations

from dataclasses import dataclass

from traceguard.domain.coverage import CoverageResult, ValidationFinding


@dataclass(frozen=True)
class RuleRun:
    coverage: list[CoverageResult]
    findings: list[ValidationFinding]

