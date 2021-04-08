import random

import pytest

from .gcd import gcd as fast


def slow(a, b):
    current_gcd = 1
    for d in range(2, min(a, b) + 1):
        if a % d == 0 and b % d == 0:
            if d > current_gcd:
                current_gcd = d

    return current_gcd


@pytest.mark.parametrize(
    "numbers",
    [random.sample(range(1, 10_000), 2) for i in range(1000)],
)
def test_stress(numbers):
    assert fast(*numbers) == slow(*numbers)
