from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from traceguard.domain.atom import RequirementAtom
from traceguard.domain.trace import TraceLink


class RequirementLevel(StrEnum):
    STAKEHOLDER = "stakeholder"
    SYSTEM = "system"
    SOFTWARE = "software"
    HARDWARE = "hardware"
    COMPONENT = "component"
    TEST = "test"


class RequirementType(StrEnum):
    FUNCTIONAL = "functional"
    INTERFACE = "interface"
    SAFETY = "safety"
    PERFORMANCE = "performance"
    CONSTRAINT = "constraint"
    VERIFICATION = "verification"
    QUALITY = "quality"


class RequirementStatus(StrEnum):
    DRAFT = "draft"
    BASELINED = "baselined"
    APPROVED = "approved"
    DEPRECATED = "deprecated"


class VerificationInfo(BaseModel):
    method: str
    criteria: str | None = None


class Requirement(BaseModel):
    id: str
    level: RequirementLevel
    type: RequirementType
    text: str
    source: str | None = None
    version: str | None = None
    status: RequirementStatus = RequirementStatus.DRAFT
    attributes: dict[str, Any] = Field(default_factory=dict)
    atoms: list[RequirementAtom] = Field(default_factory=list)
    parent_links: list[TraceLink] = Field(default_factory=list)
    verification: VerificationInfo | None = None

