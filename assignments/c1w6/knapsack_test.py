import pytest

from .knapsack import iterative, recursive


@pytest.mark.parametrize(
    "capacity, weights, expected",
    [
        (10, [11, 12, 13], 0),
        (10, [10, 1, 2], 10),
        (10, [2, 4, 8], 10),
        (10, [3, 3, 4], 10),
    ],
)
def test_basic(capacity, weights, expected):
    assert recursive(capacity, weights) == iterative(capacity, weights) == expected
