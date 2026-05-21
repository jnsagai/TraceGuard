from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class ProposalDecision(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    ACCEPTED_WITH_WARNING = "accepted_with_warning"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"


class ProposedParentLink(BaseModel):
    parent_id: str
    covered_atoms: list[str] = Field(default_factory=list)
    derivation_type: str
    rationale: str | None = None


class ProposedRequirement(BaseModel):
    id: str
    text: str
    parent_links: list[ProposedParentLink] = Field(default_factory=list)


class AIProposal(BaseModel):
    proposal_id: str
    generated_by: str
    requirements: list[ProposedRequirement] = Field(default_factory=list)


class ProposalValidationResult(BaseModel):
    proposal_id: str
    requirement_id: str
    decision: ProposalDecision
    explanation: str

