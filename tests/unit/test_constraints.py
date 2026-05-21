from hypothesis import given
from hypothesis import strategies as st

from traceguard.domain.constraint import ComparisonOperator, Constraint, ConstraintType
from traceguard.domain.constraint_logic import compare_child_to_parent
from traceguard.domain.coverage import CoverageStatus
from traceguard.parser.controlled_language import parse_numeric_constraint


def test_parse_numeric_constraints() -> None:
    assert parse_numeric_constraint("within 10 ms") is not None
    assert parse_numeric_constraint("less than 5 km/h") is not None
    assert parse_numeric_constraint("between 3 and 5 V") is not None
    assert parse_numeric_constraint("every 5 ms") is not None


@given(parent=st.floats(min_value=1, max_value=1000), child=st.floats(min_value=1, max_value=1000))
def test_upper_bound_comparison_property(parent: float, child: float) -> None:
    parent_constraint = Constraint(
        type=ConstraintType.NUMERIC,
        parameter="latency",
        operator=ComparisonOperator.LE,
        value=parent,
        unit="ms",
    )
    child_constraint = Constraint(
        type=ConstraintType.NUMERIC,
        parameter="latency",
        operator=ComparisonOperator.LE,
        value=child,
        unit="ms",
    )

    result = compare_child_to_parent(parent_constraint, child_constraint)

    if child < parent:
        assert result.status == CoverageStatus.STRONGER_THAN_PARENT
    elif child == parent:
        assert result.status == CoverageStatus.FULL
    else:
        assert result.status == CoverageStatus.WEAKER_THAN_PARENT

