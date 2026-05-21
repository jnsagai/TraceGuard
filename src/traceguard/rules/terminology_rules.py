from __future__ import annotations

from traceguard.domain.coverage import Severity, ValidationFinding
from traceguard.parser.glossary import Glossary


def validate_glossary(glossary: Glossary) -> list[ValidationFinding]:
    return [
        ValidationFinding(
            code="R-TERM-002",
            message=f"Ambiguous glossary alias: {alias}.",
            severity=Severity.HIGH,
        )
        for alias in glossary.validate_no_ambiguous_aliases()
    ]

