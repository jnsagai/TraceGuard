from __future__ import annotations

import re

from traceguard.domain.atom import AtomKind, AtomStatus, RequirementAtom, SafetyRelevance
from traceguard.domain.constraint import ComparisonOperator, Constraint
from traceguard.domain.requirement import Requirement
from traceguard.parser.controlled_language import find_vague_terms, parse_numeric_constraint
from traceguard.parser.normalizer import canonicalize, display_clean


def atomize_requirement(requirement: Requirement) -> list[RequirementAtom]:
    text = display_clean(requirement.text)
    atoms: list[RequirementAtom] = []
    vague_terms = find_vague_terms(text)
    subject, body = _split_shall(text)
    condition = _extract_condition(text)
    body_parts = _split_body(body)

    for part in body_parts:
        action, obj = _extract_action_object(part)
        constraint = parse_numeric_constraint(part)
        kind = _kind_for(part, constraint is not None)
        status = AtomStatus.NEEDS_REVIEW if vague_terms or not action else AtomStatus.AUTO_ACCEPTED
        predicate = _predicate(kind, subject, action, obj, constraint, part)
        atoms.append(
            RequirementAtom(
                id=f"{requirement.id}.A{len(atoms) + 1}",
                parent_requirement_id=requirement.id,
                kind=kind,
                subject=canonicalize(subject) if subject else None,
                action=canonicalize(action) if action else None,
                object=canonicalize(obj) if obj else None,
                condition=condition,
                constraint=constraint,
                predicate=predicate,
                atom_status=status,
            )
        )
        if constraint and kind != AtomKind.TIMING_CONSTRAINT:
            atoms.append(
                RequirementAtom(
                    id=f"{requirement.id}.A{len(atoms) + 1}",
                    parent_requirement_id=requirement.id,
                    kind=AtomKind.TIMING_CONSTRAINT,
                    subject=canonicalize(subject) if subject else None,
                    action=canonicalize(action) if action else None,
                    object=canonicalize(obj) if obj else None,
                    condition=condition,
                    constraint=constraint,
                    predicate=_predicate(
                        AtomKind.TIMING_CONSTRAINT,
                        subject,
                        action,
                        obj,
                        constraint,
                        part,
                    ),
                    atom_status=status,
                )
            )

    asil_atoms = _asil_atoms(requirement, len(atoms))
    atoms.extend(asil_atoms)
    return atoms


def _split_shall(text: str) -> tuple[str, str]:
    match = re.search(r"\bshall\b", text, flags=re.IGNORECASE)
    if not match:
        return "", text
    before = text[: match.start()].strip().strip(".,")
    after = text[match.end() :].strip(" .")
    before = re.sub(r"^(when|if|while)\b.+?,\s*", "", before, flags=re.IGNORECASE)
    before = re.sub(r"^the\s+", "", before, flags=re.IGNORECASE)
    return before, after


def _extract_condition(text: str) -> str | None:
    match = re.match(r"^\s*(when|if|while)\s+(.+?),\s+", text, flags=re.IGNORECASE)
    return display_clean(match.group(0).rstrip(", ")) if match else None


def _split_body(body: str) -> list[str]:
    body = re.sub(r"\s+with\s+ASIL-[A-D]\s+integrity", "", body, flags=re.IGNORECASE)
    parts = re.split(r"\s+\band\b\s+(?=[a-zA-Z])", body)
    return [display_clean(part.strip(" .")) for part in parts if part.strip(" .")]


def _extract_action_object(part: str) -> tuple[str | None, str | None]:
    words = part.split()
    if not words:
        return None, None
    action = words[0]
    obj = " ".join(words[1:])
    obj = re.sub(
        r"\b(within|every|<=|<|>=|>|less than|greater than)\b.*$",
        "",
        obj,
        flags=re.IGNORECASE,
    ).strip(" .")
    return action, obj or None


def _kind_for(part: str, has_constraint: bool) -> AtomKind:
    lowered = part.lower()
    if "asil-" in lowered or "integrity" in lowered:
        return AtomKind.SAFETY_INTEGRITY
    if any(word in lowered for word in ("transmit", "publish", "send", "receive")):
        return AtomKind.INTERFACE
    if has_constraint and any(word in lowered for word in ("within", "every", "ms", "s")):
        return AtomKind.TIMING_CONSTRAINT
    return AtomKind.FUNCTION


def _predicate(
    kind: AtomKind,
    subject: str,
    action: str | None,
    obj: str | None,
    constraint: Constraint | None,
    raw: str,
) -> str:
    if constraint is not None:
        op = constraint.operator
        if op == ComparisonOperator.LE:
            symbol = "<="
        elif op == ComparisonOperator.LT:
            symbol = "<"
        elif op == ComparisonOperator.GE:
            symbol = ">="
        elif op == ComparisonOperator.GT:
            symbol = ">"
        else:
            symbol = str(op)
        return (
            f"{constraint.parameter}({canonicalize(action or raw)}) "
            f"{symbol} {constraint.value} {constraint.unit or ''}"
        ).strip()
    if kind == AtomKind.INTERFACE:
        return (
            f"{canonicalize(action or 'interface')}"
            f"({canonicalize(subject)}, {canonicalize(obj or raw)})"
        )
    return (
        f"{canonicalize(action or 'require')}"
        f"({canonicalize(subject)}, {canonicalize(obj or raw)})"
    )


def _asil_atoms(requirement: Requirement, offset: int) -> list[RequirementAtom]:
    text = f"{requirement.text} {requirement.attributes.get('asil', '')}"
    match = re.search(r"ASIL[-\s]?([A-D])", text, flags=re.IGNORECASE)
    if not match:
        return []
    asil = f"ASIL-{match.group(1).upper()}"
    return [
        RequirementAtom(
            id=f"{requirement.id}.A{offset + 1}",
            parent_requirement_id=requirement.id,
            kind=AtomKind.SAFETY_INTEGRITY,
            predicate=f"safety_integrity({asil})",
            safety_relevance=SafetyRelevance(asil),
        )
    ]
