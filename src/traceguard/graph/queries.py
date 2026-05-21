from __future__ import annotations

from traceguard.domain.requirement import Requirement
from traceguard.domain.trace import TraceLink


def parent_requirements(
    requirements: list[Requirement],
    links: list[TraceLink],
) -> list[Requirement]:
    sources = {link.source_id for link in links}
    return sorted((req for req in requirements if req.id in sources), key=lambda req: req.id)
