from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel


class ConstraintType(StrEnum):
    NUMERIC = "numeric"
    ENUMERATION = "enumeration"
    TEXT = "text"


class ComparisonOperator(StrEnum):
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    IN = "in"
    NOT_IN = "not_in"
    BETWEEN = "between"
    CONTAINS = "contains"


class Constraint(BaseModel):
    type: ConstraintType
    parameter: str
    operator: ComparisonOperator
    value: float | int | str | list[float]
    unit: str | None = None
    context: str | None = None

