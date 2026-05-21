from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from traceguard.parser.normalizer import canonicalize


@dataclass(frozen=True)
class GlossaryTerm:
    canonical: str
    type: str
    aliases: tuple[str, ...]


@dataclass(frozen=True)
class ResolveResult:
    status: str
    canonical: str | None
    message: str


class Glossary:
    def __init__(self, terms: dict[str, GlossaryTerm]) -> None:
        self.terms = terms
        self._index: dict[str, list[str]] = {}
        for canonical, term in terms.items():
            self._index.setdefault(canonicalize(canonical), []).append(canonical)
            for alias in term.aliases:
                self._index.setdefault(canonicalize(alias), []).append(canonical)

    @classmethod
    def from_yaml(cls, path: Path) -> Glossary:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        raw_terms = data.get("terms", {})
        terms = {
            canonicalize(name): GlossaryTerm(
                canonical=canonicalize(name),
                type=str(payload.get("type", "unknown")),
                aliases=tuple(str(alias) for alias in payload.get("aliases", [])),
            )
            for name, payload in raw_terms.items()
        }
        return cls(terms)

    @classmethod
    def empty(cls) -> Glossary:
        return cls({})

    def resolve(self, term: str) -> ResolveResult:
        key = canonicalize(term)
        matches = sorted(set(self._index.get(key, [])))
        if len(matches) == 1:
            return ResolveResult("resolved", matches[0], f"'{term}' resolves to {matches[0]}.")
        if len(matches) > 1:
            return ResolveResult("ambiguous", None, f"'{term}' matches multiple terms: {matches}.")
        return ResolveResult("unknown", None, f"'{term}' is not defined in the glossary.")

    def validate_no_ambiguous_aliases(self) -> list[str]:
        return [alias for alias, matches in sorted(self._index.items()) if len(set(matches)) > 1]

