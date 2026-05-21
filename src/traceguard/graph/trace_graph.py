from __future__ import annotations

import networkx as nx

from traceguard.domain.requirement import Requirement
from traceguard.domain.trace import TraceLink, TraceLinkType


class TraceGraph:
    def __init__(self, requirements: list[Requirement], links: list[TraceLink]) -> None:
        self.graph: nx.DiGraph[str] = nx.DiGraph()
        self.links = links
        for requirement in requirements:
            self.graph.add_node(requirement.id, requirement=requirement)
        for link in links:
            self.graph.add_edge(
                link.source_id,
                link.target_id,
                link=link,
                link_type=link.link_type.value,
            )

    def children(self, requirement_id: str) -> list[str]:
        return sorted(self.graph.successors(requirement_id))

    def parents(self, requirement_id: str) -> list[str]:
        return sorted(self.graph.predecessors(requirement_id))

    def self_derived_requirements(self) -> list[str]:
        return sorted(
            link.target_id for link in self.links if link.link_type == TraceLinkType.SELF_DERIVED
        )

    def trace_path(self, source_id: str, target_id: str) -> list[str] | None:
        try:
            return list(nx.shortest_path(self.graph, source_id, target_id))
        except nx.NetworkXNoPath:
            return None
