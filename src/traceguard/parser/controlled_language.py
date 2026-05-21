from __future__ import annotations

import re

from traceguard.domain.constraint import ComparisonOperator, Constraint, ConstraintType

SUPPORTED_UNITS = {
    "ns",
    "us",
    "ms",
    "s",
    "m/s",
    "km/h",
    "mm",
    "cm",
    "m",
    "km",
    "°C",
    "K",
    "Hz",
    "kHz",
    "%",
    "mV",
    "V",
    "mA",
    "A",
}
VAGUE_TERMS = {
    "fast",
    "robust",
    "optimized",
    "minimized",
    "user-friendly",
    "as soon as possible",
    "where appropriate",
    "sufficient",
    "adequate",
    "high performance",
}


def find_vague_terms(text: str) -> list[str]:
    lower = text.lower()
    return sorted(term for term in VAGUE_TERMS if term in lower)


def parse_numeric_constraint(text: str) -> Constraint | None:
    unit = r"(ns|us|ms|s|m/s|km/h|mm|cm|m|km|°C|K|Hz|kHz|%|mV|V|mA|A)"
    patterns: list[tuple[str, ComparisonOperator, str]] = [
        (rf"within\s+(\d+(?:\.\d+)?)\s*{unit}", ComparisonOperator.LE, "latency"),
        (rf"every\s+(\d+(?:\.\d+)?)\s*{unit}", ComparisonOperator.LE, "period"),
        (rf"<=\s*(\d+(?:\.\d+)?)\s*{unit}", ComparisonOperator.LE, "constraint"),
        (rf"<\s*(\d+(?:\.\d+)?)\s*{unit}", ComparisonOperator.LT, "constraint"),
        (rf">=\s*(\d+(?:\.\d+)?)\s*{unit}", ComparisonOperator.GE, "constraint"),
        (rf">\s*(\d+(?:\.\d+)?)\s*{unit}", ComparisonOperator.GT, "constraint"),
        (rf"less than\s+(\d+(?:\.\d+)?)\s*{unit}", ComparisonOperator.LT, "constraint"),
        (rf"greater than\s+(\d+(?:\.\d+)?)\s*{unit}", ComparisonOperator.GT, "constraint"),
    ]
    for pattern, operator, parameter in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            raw_value = float(match.group(1))
            value: float | int = int(raw_value) if raw_value.is_integer() else raw_value
            return Constraint(
                type=ConstraintType.NUMERIC,
                parameter=parameter,
                operator=operator,
                value=value,
                unit=match.group(2),
                context=match.group(0),
            )

    between = re.search(
        rf"between\s+(\d+(?:\.\d+)?)\s+and\s+(\d+(?:\.\d+)?)\s*{unit}",
        text,
        flags=re.IGNORECASE,
    )
    if between:
        return Constraint(
            type=ConstraintType.NUMERIC,
            parameter="range",
            operator=ComparisonOperator.BETWEEN,
            value=[float(between.group(1)), float(between.group(2))],
            unit=between.group(3),
            context=between.group(0),
        )
    return None

