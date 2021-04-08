import random

import pytest

from .fibonacci_huge import get_fibonacci_huge as fast
from .fibonacci_huge import get_pisano_period


@pytest.mark.parametrize(
    "m, expected",
    [
        (2, list(map(int, "011"))),
        (3, list(map(int, "01120221"))),
        (4, list(map(int, "011231"))),
        (5, list(map(int, "01123033140443202241"))),
        (6, list(map(int, "011235213415055431453251"))),
    ],
)
def test_get_pisano_period(m, expected):
    assert get_pisano_period(m) == expected


def slow(n, m):
    if n <= 1:
        return n

    previous = 0
    current = 1

    for _ in range(n - 1):
        previous, current = current, previous + current

    return current % m


@pytest.mark.parametrize(
    "numbers",
    [(random.randint(1, 10_000), random.randint(2, 100)) for i in range(1000)],
)
def test_stress(numbers):
    assert fast(*numbers) == slow(*numbers)
