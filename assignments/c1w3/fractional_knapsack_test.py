import pytest

from .fractional_knapsack import get_optimal_value


@pytest.mark.parametrize(
    "capacity, weights, values, expected",
    [
        pytest.param(
            10, [3, 3, 3], [10, 20, 30], 60, id="less total weights than capacity"
        ),
        pytest.param(10, [5, 5, 10], [10, 20, 50], 50, id="one item knapsack"),
        pytest.param(10, [5, 6, 7], [15, 24, 28], 40, id="general"),
    ],
)
def test_basic(capacity, weights, values, expected):
    assert get_optimal_value(capacity, weights, values) == expected
