from __future__ import annotations

import re
from pathlib import Path

from traceguard.domain.requirement import Requirement
from traceguard.domain.trace import TraceLink, TraceLinkType


def derive_links_from_markdown(
    requirements: list[Requirement],
    derivation_file: Path,
) -> list[TraceLink]:
    """Extract parent-child trace links from grouped derivation Markdown tables."""
    atom_ids_by_parent = {
        requirement.id: [atom.id for atom in requirement.atoms] for requirement in requirements
    }
    requirement_ids = {requirement.id for requirement in requirements}
    links: list[TraceLink] = []
    current_parent_id: str | None = None

    for line in derivation_file.read_text(encoding="utf-8").splitlines():
        parent_heading = re.match(r"^##\s+(ROC-SYS-\d{3})\s*$", line.strip())
        if parent_heading:
            current_parent_id = parent_heading.group(1)
            continue
        if current_parent_id is None:
            continue
        child_match = re.match(r"^\|\s*(ROC-SWR-\d{3}-\d{2})\s*\|", line.strip())
        if not child_match:
            continue
        child_id = child_match.group(1)
        if child_id not in requirement_ids:
            continue
        links.append(
            TraceLink(
                source_id=current_parent_id,
                target_id=child_id,
                link_type=TraceLinkType.DECOMPOSES,
                covered_atom_ids=atom_ids_by_parent.get(current_parent_id, []),
                rationale=(
                    f"{child_id} is listed under {current_parent_id} in the derivation "
                    "Markdown table."
                ),
            )
        )
    return links
