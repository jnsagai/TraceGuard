from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel

from traceguard.domain.constraint import Constraint


class AtomKind(StrEnum):
    FUNCTION = "function"
    INTERFACE = "interface"
    TIMING_CONSTRAINT = "timing_constraint"
    RANGE_CONSTRAINT = "range_constraint"
    ACCURACY_CONSTRAINT = "accuracy_constraint"
    CAPACITY_CONSTRAINT = "capacity_constraint"
    SAFETY_INTEGRITY = "safety_integrity"
    DIAGNOSTIC = "diagnostic"
    FAULT_REACTION = "fault_reaction"
    AVAILABILITY = "availability"
    SECURITY = "security"
    USABILITY = "usability"
    ENVIRONMENTAL = "environmental"
    VERIFICATION = "verification"
    ALLOCATION = "allocation"


class SafetyRelevance(StrEnum):
    QM = "QM"
    ASIL_A = "ASIL-A"
    ASIL_B = "ASIL-B"
    ASIL_C = "ASIL-C"
    ASIL_D = "ASIL-D"


class AtomStatus(StrEnum):
    AUTO_ACCEPTED = "auto_accepted"
    NEEDS_REVIEW = "needs_review"
    REJECTED = "rejected"
    MANUAL = "manual"


class RequirementAtom(BaseModel):
    id: str
    parent_requirement_id: str
    kind: AtomKind
    subject: str | None = None
    action: str | None = None
    object: str | None = None
    condition: str | None = None
    constraint: Constraint | None = None
    predicate: str
    safety_relevance: SafetyRelevance | None = None
    atom_status: AtomStatus = AtomStatus.AUTO_ACCEPTED

