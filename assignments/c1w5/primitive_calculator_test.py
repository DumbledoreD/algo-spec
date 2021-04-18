import pytest

from .primitive_calculator import iterative, iterative_plus, recursive


@pytest.mark.parametrize("n", list(range(1000)))
def test_basic(n):
    assert recursive(n) == iterative(n)


@pytest.mark.parametrize(
    "n, expected",
    [
        (1, [1]),
        (2, [1, 2]),
        (3, [1, 3]),
        (4, [1, 3, 4]),
        (5, [1, 3, 4, 5]),
        (6, [1, 3, 6]),
        (7, [1, 3, 6, 7]),
        (8, [1, 3, 4, 8]),
        (9, [1, 3, 9]),
        (10, [1, 3, 9, 10]),
    ],
)
def test_iterative_plus(n, expected):
    assert iterative_plus(n) == expected
