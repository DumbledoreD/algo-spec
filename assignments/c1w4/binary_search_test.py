import pytest

from .binary_search import binary_search


@pytest.mark.parametrize(
    "a, x, expected",
    [
        ([1, 5, 8, 12, 13], 8, 2),
        ([1, 5, 8, 12, 13], 1, 0),
        ([1, 5, 8, 12, 13], 23, -1),
        ([1, 5, 8, 12, 13], 11, -1),
        ([1, 5, 8, 12, 13], 13, 4),
        ([1, 5, 8, 12, 13, 17], 17, 5),
        ([1, 5, 8, 12, 13, 17], 1, 0),
    ],
)
def test_basic(a, x, expected):
    assert binary_search(a, x) == expected
