from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class TraceLinkType(StrEnum):
    DERIVES = "derives"
    REFINES = "refines"
    DECOMPOSES = "decomposes"
    ALLOCATES = "allocates"
    SATISFIES = "satisfies"
    VERIFIES = "verifies"
    CONSTRAINS = "constrains"
    ASSUMES = "assumes"
    MITIGATES = "mitigates"
    DUPLICATES = "duplicates"
    CONFLICTS = "conflicts"
    SELF_DERIVED = "self_derived"


class TraceOrigin(StrEnum):
    MANUAL = "manual"
    IMPORTED = "imported"
    AI_PROPOSED = "ai_proposed"
    TOOL_GENERATED = "tool_generated"
    APPROVED_BY_REVIEW = "approved_by_review"


class ReviewStatus(StrEnum):
    UNREVIEWED = "unreviewed"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"


class TraceLink(BaseModel):
    source_id: str
    target_id: str
    link_type: TraceLinkType
    covered_atom_ids: list[str] = Field(default_factory=list)
    rationale: str | None = None
    author: str | None = None
    origin: TraceOrigin = TraceOrigin.MANUAL
    review_status: ReviewStatus = ReviewStatus.UNREVIEWED

