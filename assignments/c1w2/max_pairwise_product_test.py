import random

import pytest

from .max_pairwise_product import max_pairwise_product as fast


def slow(numbers):
    n = len(numbers)
    max_product = 0
    for first in range(n):
        for second in range(first + 1, n):
            max_product = max(max_product, numbers[first] * numbers[second])

    return max_product


@pytest.mark.parametrize(
    "numbers",
    [
        [1, 2, 3],
        [1, 3, 3],
    ],
)
def test_basic(numbers):
    assert fast(numbers) == slow(numbers)


@pytest.mark.parametrize(
    "numbers",
    [random.sample(range(1_000), random.randint(1, 100)) for i in range(1_000)],
)
def test_stress(numbers):
    assert fast(numbers) == slow(numbers)
