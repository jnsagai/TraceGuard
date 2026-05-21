from traceguard.domain.atom import AtomKind, RequirementAtom
from traceguard.domain.coverage import CoverageResult, CoverageStatus, Severity
from traceguard.domain.requirement import Requirement, RequirementLevel, RequirementType


def test_requirement_serializes_round_trip() -> None:
    requirement = Requirement(
        id="SYS-REQ-001",
        level=RequirementLevel.SYSTEM,
        type=RequirementType.FUNCTIONAL,
        text="The system shall detect a fault.",
        atoms=[
            RequirementAtom(
                id="SYS-REQ-001.A1",
                parent_requirement_id="SYS-REQ-001",
                kind=AtomKind.FUNCTION,
                predicate="detect(system, fault)",
            )
        ],
    )

    restored = Requirement.model_validate_json(requirement.model_dump_json())

    assert restored == requirement


def test_coverage_result_contains_auditable_fields() -> None:
    result = CoverageResult(
        parent_requirement_id="SYS-REQ-001",
        parent_atom_id="SYS-REQ-001.A1",
        status=CoverageStatus.MISSING,
        child_requirement_ids=[],
        child_atom_ids=[],
        rule_id="R-ATOM-001",
        explanation="No child covers the atom.",
        severity=Severity.HIGH,
    )

    assert result.rule_id == "R-ATOM-001"
    assert "No child" in result.explanation

