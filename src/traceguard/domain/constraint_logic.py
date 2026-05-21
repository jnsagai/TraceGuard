from __future__ import annotations

from dataclasses import dataclass

from traceguard.domain.constraint import ComparisonOperator, Constraint
from traceguard.domain.coverage import CoverageStatus

TIME_FACTORS = {"ns": 0.000001, "us": 0.001, "ms": 1.0, "s": 1000.0}
SPEED_FACTORS = {"m/s": 3.6, "km/h": 1.0}
DISTANCE_FACTORS = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
FREQUENCY_FACTORS = {"Hz": 1.0, "kHz": 1000.0}
VOLTAGE_FACTORS = {"mV": 0.001, "V": 1.0}
CURRENT_FACTORS = {"mA": 0.001, "A": 1.0}
SAME_FACTORS = {"%": 1.0, "K": 1.0, "C": 1.0, "degC": 1.0}
UNIT_FACTORS = {
    **TIME_FACTORS,
    **SPEED_FACTORS,
    **DISTANCE_FACTORS,
    **FREQUENCY_FACTORS,
    **VOLTAGE_FACTORS,
    **CURRENT_FACTORS,
    **SAME_FACTORS,
}


@dataclass(frozen=True)
class ConstraintComparison:
    status: CoverageStatus
    explanation: str


def normalize_value(value: float | int, unit: str | None) -> float:
    if unit is None:
        return float(value)
    if unit not in UNIT_FACTORS:
        raise ValueError(f"Unsupported unit: {unit}")
    return float(value) * UNIT_FACTORS[unit]


def _numeric(value: float | int | str | list[float]) -> float:
    if isinstance(value, list):
        raise TypeError("Range constraints are not supported by scalar comparison.")
    return float(value)


def compare_child_to_parent(parent: Constraint, child: Constraint) -> ConstraintComparison:
    if parent.unit and child.unit:
        try:
            parent_value = normalize_value(_numeric(parent.value), parent.unit)
            child_value = normalize_value(_numeric(child.value), child.unit)
        except (TypeError, ValueError) as exc:
            return ConstraintComparison(CoverageStatus.MANUAL_REVIEW_REQUIRED, str(exc))
    else:
        parent_value = _numeric(parent.value)
        child_value = _numeric(child.value)

    if parent.operator in {ComparisonOperator.LE, ComparisonOperator.LT}:
        if child.operator not in {ComparisonOperator.LE, ComparisonOperator.LT}:
            return ConstraintComparison(CoverageStatus.MANUAL_REVIEW_REQUIRED, "Operator mismatch.")
        if child_value < parent_value:
            return ConstraintComparison(
                CoverageStatus.STRONGER_THAN_PARENT,
                f"Child limit {child.value} {child.unit or ''} is stricter than parent "
                f"{parent.value} {parent.unit or ''}.",
            )
        if child_value == parent_value:
            return ConstraintComparison(CoverageStatus.FULL, "Child limit equals parent limit.")
        return ConstraintComparison(
            CoverageStatus.WEAKER_THAN_PARENT,
            "Child upper bound is weaker.",
        )

    if parent.operator in {ComparisonOperator.GE, ComparisonOperator.GT}:
        if child.operator not in {ComparisonOperator.GE, ComparisonOperator.GT}:
            return ConstraintComparison(CoverageStatus.MANUAL_REVIEW_REQUIRED, "Operator mismatch.")
        if child_value > parent_value:
            return ConstraintComparison(
                CoverageStatus.STRONGER_THAN_PARENT, "Child lower bound is stricter than parent."
            )
        if child_value == parent_value:
            return ConstraintComparison(
                CoverageStatus.FULL,
                "Child lower bound equals parent limit.",
            )
        return ConstraintComparison(
            CoverageStatus.WEAKER_THAN_PARENT,
            "Child lower bound is weaker.",
        )

    return ConstraintComparison(CoverageStatus.MANUAL_REVIEW_REQUIRED, "Unsupported comparison.")
