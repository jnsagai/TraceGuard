from __future__ import annotations

import re
from pathlib import Path

from traceguard.domain.requirement import Requirement, RequirementLevel, RequirementType
from traceguard.parser.normalizer import display_clean


def import_markdown_requirements(path: Path) -> list[Requirement]:
    text = path.read_text(encoding="utf-8")
    table_requirements = _import_table_requirements(text, path)
    if table_requirements:
        return table_requirements

    blocks = re.split(r"^##\s+", text, flags=re.MULTILINE)
    requirements: list[Requirement] = []
    for block in blocks[1:]:
        lines = block.strip().splitlines()
        if not lines:
            continue
        req_id = lines[0].strip()
        attrs: dict[str, str] = {}
        body_lines: list[str] = []
        for line in lines[1:]:
            attr_match = re.match(r"^([A-Za-z_ -]+):\s*(.+)$", line.strip())
            if attr_match and not body_lines:
                key = attr_match.group(1).strip().lower().replace(" ", "_")
                attrs[key] = attr_match.group(2).strip()
            elif line.strip():
                body_lines.append(line.strip())
        if not body_lines:
            raise ValueError(f"Requirement {req_id} in {path} has no text.")
        requirements.append(
            Requirement(
                id=req_id,
                level=RequirementLevel(attrs.get("level", "system").lower()),
                type=RequirementType(attrs.get("type", "functional").lower()),
                text=display_clean(" ".join(body_lines)),
                source=str(path),
                attributes={k: v for k, v in attrs.items() if k not in {"level", "type"}},
            )
        )
    return requirements


def _import_table_requirements(text: str, path: Path) -> list[Requirement]:
    requirements: list[Requirement] = []
    current_parent_id: str | None = None
    lines = text.splitlines()
    for line in lines:
        parent_heading = re.match(r"^##\s+(ROC-SYS-\d{3})\s*$", line.strip())
        if parent_heading:
            current_parent_id = parent_heading.group(1)
            continue

        cells = _table_cells(line)
        if len(cells) < 2:
            continue
        if cells[0] in {"ID", "Software Requirement ID", "---"}:
            continue

        if re.fullmatch(r"ROC-SYS-\d{3}", cells[0]) and len(cells) >= 2:
            requirements.append(
                Requirement(
                    id=cells[0],
                    level=RequirementLevel.SYSTEM,
                    type=_infer_type(cells[1]),
                    text=_normalize_symbols(cells[1]),
                    source=str(path),
                )
            )
            continue

        if re.fullmatch(r"ROC-SWR-\d{3}-\d{2}", cells[0]) and len(cells) >= 3:
            attributes = {"allocation_area": cells[1]}
            if len(cells) >= 4:
                attributes["suggested_verification"] = cells[3]
            if current_parent_id:
                attributes["derived_from"] = current_parent_id
            requirements.append(
                Requirement(
                    id=cells[0],
                    level=RequirementLevel.SOFTWARE,
                    type=_infer_type(cells[2], cells[1]),
                    text=_normalize_symbols(cells[2]),
                    source=str(path),
                    attributes=attributes,
                )
            )
    return requirements


def _table_cells(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def _normalize_symbols(text: str) -> str:
    normalized = text.replace("≤", "<=").replace("≥", ">=")
    normalized = normalized.replace("±", "+/-").replace("°", " deg ")
    normalized = normalized.replace("â‰¤", "<=").replace("Â±", "+/-")
    normalized = normalized.replace("Â°C", "degC").replace("â€“", "-")
    return display_clean(normalized)


def _infer_type(text: str, allocation_area: str = "") -> RequirementType:
    combined = f"{text} {allocation_area}".lower()
    if any(word in combined for word in ("diagnostic", "fault", "safe state", "safety")):
        return RequirementType.SAFETY
    if any(word in combined for word in ("interface", "spi", "output", "report", "host")):
        return RequirementType.INTERFACE
    if any(word in combined for word in ("secure", "authenticated", "access control")):
        return RequirementType.CONSTRAINT
    if any(word in combined for word in ("accuracy", "resolution", "latency", "within")):
        return RequirementType.PERFORMANCE
    return RequirementType.FUNCTIONAL
