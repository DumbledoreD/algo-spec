import pytest

from .lcs3 import iterative, recursive


@pytest.mark.parametrize(
    "a, b, c, expected",
    [
        ([1, 2, 3], [2, 1, 3], [1, 3, 5], 2),
        ([8, 3, 2, 1, 7], [8, 2, 1, 3, 8, 10, 7], [6, 8, 3, 1, 4, 7], 3),
        ([0], [0], [0], 1),
        ([1], [2], [3], 0),
        ([0], [1], [1], 0),
        ([1], [0], [0], 0),
        ([0, 1], [1, 0], [1, 0], 1),
        ([0, 1, 2], [1, 0, 2], [1, 2, 0], 2),
    ],
)
def test_basic(a, b, c, expected):
    assert recursive(a, b, c) == iterative(a, b, c) == expected
