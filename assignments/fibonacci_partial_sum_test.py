import random

import pytest

from .fibonacci_partial_sum import fibonacci_partial_sum as fast


def slow(m, n):
    fib_sum = 0

    current = 0
    next = 1

    for i in range(n + 1):
        if i >= m:
            fib_sum += current

        current, next = next, current + next

    return fib_sum % 10


def test_large_num():
    assert fast(10 ** 13, 10 ** 14)


@pytest.mark.parametrize(
    "m, n",
    [sorted(random.sample(range(1000), 2)) for i in range(1000)],
)
def test_stress(m, n):
    assert fast(m, n) == slow(m, n)
