import pytest

from .placing_parentheses import iterative, recursive


@pytest.mark.parametrize(
    "expression, min_val, max_val",
    [
        ("1+2", 3, 3),
        ("1+2+3", 6, 6),
        ("1-2-3", -4, 2),
        ("1-2*3", -5, -3),
        ("5-8+7*4-8+9", -94, 200),
    ],
)
def test_basic(expression, min_val, max_val):
    digits, operators = expression[::2], expression[1::2]
    assert (
        recursive(digits, operators)
        == iterative(digits, operators)
        == (min_val, max_val)
    )
