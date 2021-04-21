import pytest

from .partition3 import iterative, recursive


@pytest.mark.parametrize(
    "a, expected",
    [
        ([3], False),
        ([3, 3, 3], True),
        ([3, 3, 3, 3], False),
        ([17, 59, 34, 57, 17, 23, 67, 1, 18, 2, 59], True),
        ([1, 2, 3, 4, 5, 5, 7, 7, 8, 10, 12, 19, 25], True),
    ],
)
def test_basic(a, expected):
    assert recursive(a) == iterative(a) == expected
