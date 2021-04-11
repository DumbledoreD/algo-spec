import pytest

from .different_summands import optimal_summands


@pytest.mark.parametrize(
    "n, expected",
    [
        (1, [1]),
        (2, [2]),
        (3, [1, 2]),
        (4, [1, 3]),
        (5, [1, 4]),
        (6, [1, 2, 3]),
    ],
)
def test_basic(n, expected):
    assert optimal_summands(n) == expected
