from __future__ import annotations

from traceguard.ai.schema import AIProposal, ProposalDecision, ProposalValidationResult
from traceguard.domain.requirement import Requirement

ALLOWED_DERIVATION_TYPES = {"functional_decomposition", "allocation", "constraint_refinement"}


def validate_ai_proposal(
    proposal: AIProposal,
    parent_requirements: list[Requirement],
) -> list[ProposalValidationResult]:
    parent_ids = {requirement.id for requirement in parent_requirements}
    atom_ids = {atom.id for requirement in parent_requirements for atom in requirement.atoms}
    results: list[ProposalValidationResult] = []
    for requirement in proposal.requirements:
        decision = ProposalDecision.ACCEPTED
        messages: list[str] = []
        for link in requirement.parent_links:
            if link.parent_id not in parent_ids:
                decision = ProposalDecision.REJECTED
                messages.append(f"Unknown parent requirement {link.parent_id}.")
            unknown_atoms = [atom for atom in link.covered_atoms if atom not in atom_ids]
            if unknown_atoms:
                decision = ProposalDecision.REJECTED
                messages.append(f"Unknown covered atoms: {', '.join(unknown_atoms)}.")
            if link.derivation_type not in ALLOWED_DERIVATION_TYPES:
                decision = ProposalDecision.MANUAL_REVIEW_REQUIRED
                messages.append(f"Unsupported derivation type {link.derivation_type}.")
            if link.covered_atoms and not link.rationale:
                decision = ProposalDecision.MANUAL_REVIEW_REQUIRED
                messages.append("Rationale is required for covered atoms.")
        if not messages:
            messages.append(
                "Proposal references valid parents, atoms, derivation type, and rationale."
            )
        results.append(
            ProposalValidationResult(
                proposal_id=proposal.proposal_id,
                requirement_id=requirement.id,
                decision=decision,
                explanation=" ".join(messages),
            )
        )
    return results
