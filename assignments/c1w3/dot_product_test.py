import itertools
import math
import random

import pytest

from .dot_product import max_dot_product


def slow(a, b):
    dot_product = -math.inf
    for a_p in itertools.permutations(a):
        for b_p in itertools.permutations(b):
            dot_product = max(dot_product, sum(a_i * b_i for a_i, b_i in zip(a_p, b_p)))
    return dot_product


@pytest.mark.parametrize(
    "a, b, expected",
    [
        pytest.param([2], [3], 6, id="simple"),
        pytest.param([1, 2, 3], [1, 2, 3], 14, id="all positives"),
        pytest.param([-1, -2, -3], [-1, -2, -3], 14, id="all negatives"),
        pytest.param(
            [1, 2, 3], [-1, -2, -3], -10, id="all positives and all negatives"
        ),
        pytest.param([1, 2, 3], [1, -2, -3], -4, id="mixed"),
    ],
)
def test_basic(a, b, expected):
    assert max_dot_product(a, b) == expected


@pytest.mark.parametrize(
    "a, b",
    [
        (
            random.sample(range(-(10 ** 5), 10 ** 5), 5),
            random.sample(range(-(10 ** 5), 10 ** 5), 5),
        )
        for i in range(1000)
    ],
)
def test_stress(a, b):
    assert max_dot_product(a, b) == slow(a, b)
