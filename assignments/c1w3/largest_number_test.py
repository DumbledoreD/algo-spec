import itertools
import random

import pytest

from .largest_number import largest_number


def slow(a):
    max_num = 0
    for a_p in itertools.permutations(a):
        max_num = max(max_num, int("".join(str(d) for d in a_p)))

    return str(max_num)


@pytest.mark.parametrize(
    "a, expected",
    [
        pytest.param([1, 2, 3], "321", id="1-digit"),
        pytest.param([2, 23, 3], "3232", id="2-digit"),
        pytest.param([2, 23, 3, 210], "3232210", id="3-digit"),
    ],
)
def test_basic(a, expected):
    assert largest_number(a) == expected


@pytest.mark.parametrize(
    "a",
    [random.sample(range(1, 10 ** 3), 5) for i in range(1000)],
)
def test_stress(a):
    assert largest_number(a) == slow(a)
