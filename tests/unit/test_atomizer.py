from traceguard.domain.atom import AtomKind
from traceguard.domain.requirement import Requirement, RequirementLevel, RequirementType
from traceguard.parser.atomizer import atomize_requirement


def test_atomizer_extracts_compound_atoms_and_asil() -> None:
    requirement = Requirement(
        id="SYS-REQ-001",
        level=RequirementLevel.SYSTEM,
        type=RequirementType.FUNCTIONAL,
        text=(
            "The braking system shall detect pedal actuation within 10 ms and transmit "
            "the braking request to the Vehicle Motion Controller with ASIL-B integrity."
        ),
    )

    atoms = atomize_requirement(requirement)

    assert [atom.id for atom in atoms] == ["SYS-REQ-001.A1", "SYS-REQ-001.A2", "SYS-REQ-001.A3"]
    assert atoms[0].constraint is not None
    assert atoms[1].kind == AtomKind.INTERFACE
    assert atoms[2].kind == AtomKind.SAFETY_INTEGRITY


def test_atomizer_flags_vague_wording() -> None:
    requirement = Requirement(
        id="SW-REQ-013",
        level=RequirementLevel.SOFTWARE,
        type=RequirementType.PERFORMANCE,
        text="The Brake Input SWC shall detect pedal actuation as soon as possible.",
    )

    atoms = atomize_requirement(requirement)

    assert atoms[0].atom_status.value == "needs_review"

