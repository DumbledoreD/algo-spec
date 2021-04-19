import pytest

from .lcs2 import iterative, recursive


@pytest.mark.parametrize(
    "a, b, expected",
    [
        ([1], [4], 0),
        ([2, 7, 5], [2, 5], 2),
        ([2, 7, 8, 3], [5, 2, 8, 7], 2),
    ],
)
def test_basic(a, b, expected):
    assert recursive(a, b) == iterative(a, b) == expected
