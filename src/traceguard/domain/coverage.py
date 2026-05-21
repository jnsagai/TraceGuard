from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel


class CoverageStatus(StrEnum):
    FULL = "full"
    PARTIAL = "partial"
    MISSING = "missing"
    CONFLICTING = "conflicting"
    WEAKER_THAN_PARENT = "weaker_than_parent"
    STRONGER_THAN_PARENT = "stronger_than_parent"
    OVER_SPECIFIED = "over_specified"
    AMBIGUOUS = "ambiguous"
    UNVERIFIABLE = "unverifiable"
    NOT_APPLICABLE = "not_applicable"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"


class Severity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CoverageResult(BaseModel):
    parent_requirement_id: str
    parent_atom_id: str
    status: CoverageStatus
    child_requirement_ids: list[str]
    child_atom_ids: list[str]
    rule_id: str
    explanation: str
    recommended_action: str | None = None
    severity: Severity


class ValidationFinding(BaseModel):
    code: str
    message: str
    severity: Severity
    file: str | None = None
    line: int | None = None

