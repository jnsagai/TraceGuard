from __future__ import annotations

from traceguard.domain.atom import AtomKind, RequirementAtom
from traceguard.domain.constraint_logic import compare_child_to_parent
from traceguard.domain.coverage import CoverageResult, CoverageStatus, Severity
from traceguard.domain.requirement import Requirement
from traceguard.domain.trace import TraceLink


def run_atom_coverage(
    requirements: list[Requirement],
    links: list[TraceLink],
) -> list[CoverageResult]:
    by_id = {requirement.id: requirement for requirement in requirements}
    results: list[CoverageResult] = []
    for parent in sorted(requirements, key=lambda req: req.id):
        parent_links = [link for link in links if link.source_id == parent.id]
        if not parent_links:
            continue
        for atom in parent.atoms:
            covering = [link for link in parent_links if atom.id in link.covered_atom_ids]
            if not covering:
                results.append(
                    CoverageResult(
                        parent_requirement_id=parent.id,
                        parent_atom_id=atom.id,
                        status=CoverageStatus.MISSING,
                        child_requirement_ids=[],
                        child_atom_ids=[],
                        rule_id="R-ATOM-001",
                        explanation=f"No child atom or approved rationale covers {atom.id}.",
                        recommended_action=(
                            "Add a child requirement, allocation, or formal exclusion."
                        ),
                        severity=Severity.HIGH,
                    )
                )
                continue
            child_ids = sorted({link.target_id for link in covering})
            child_atoms = [a for cid in child_ids for a in by_id[cid].atoms]
            matched_child_atom_ids = _compatible_child_atom_ids(atom.kind, child_atoms)
            status = CoverageStatus.FULL
            rule_id = "R-ATOM-001"
            severity = Severity.INFO
            explanation = f"{atom.id} is covered by trace link(s) to {', '.join(child_ids)}."

            if atom.constraint:
                comparable = [
                    child_atom.constraint
                    for child_atom in child_atoms
                    if child_atom.constraint is not None
                ]
                if comparable:
                    comparison = compare_child_to_parent(
                        atom.constraint,
                        comparable[0],
                    )
                    status = comparison.status
                    rule_id = "R-CONSTRAINT-001"
                    explanation = comparison.explanation
                    severity = Severity.MEDIUM if status != CoverageStatus.FULL else Severity.INFO
                    if status == CoverageStatus.STRONGER_THAN_PARENT:
                        severity = Severity.LOW
                else:
                    status = CoverageStatus.PARTIAL
                    rule_id = "R-CONSTRAINT-002"
                    explanation = (
                        f"{atom.id} has a numeric constraint but no linked child constraint."
                    )
                    severity = Severity.MEDIUM

            if atom.kind == AtomKind.SAFETY_INTEGRITY and not _has_safety_child(child_atoms):
                status = CoverageStatus.PARTIAL
                rule_id = "R-SAFETY-001"
                explanation = (
                    f"{atom.id} covers safety integrity only through rationale; review evidence."
                )
                severity = Severity.MEDIUM

            results.append(
                CoverageResult(
                    parent_requirement_id=parent.id,
                    parent_atom_id=atom.id,
                    status=status,
                    child_requirement_ids=child_ids,
                    child_atom_ids=matched_child_atom_ids or [a.id for a in child_atoms],
                    rule_id=rule_id,
                    explanation=explanation,
                    recommended_action=_action_for(status),
                    severity=severity,
                )
            )
    return results


def _compatible_child_atom_ids(kind: AtomKind, child_atoms: list[RequirementAtom]) -> list[str]:
    return sorted(atom.id for atom in child_atoms if atom.kind == kind)


def _has_safety_child(child_atoms: list[RequirementAtom]) -> bool:
    return any(atom.kind == AtomKind.SAFETY_INTEGRITY for atom in child_atoms)


def _action_for(status: CoverageStatus) -> str | None:
    if status in {CoverageStatus.FULL, CoverageStatus.STRONGER_THAN_PARENT}:
        return None
    if status == CoverageStatus.WEAKER_THAN_PARENT:
        return "Tighten the child constraint or document an approved exception."
    if status == CoverageStatus.PARTIAL:
        return "Add missing child atoms or review rationale."
    return "Review and correct the trace or requirement."
