import random

import pytest

from .lcm import lcm as fast


def slow(a, b):
    for i in range(1, a * b + 1):
        if i % a == 0 and i % b == 0:
            return i

    return a * b


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 1, 1),
        (6, 8, 24),
        (761457, 614573, 467970912861),
    ],
)
def test_basic(a, b, expected):
    result = fast(a, b)
    assert type(result) == type(expected)
    assert result == expected


@pytest.mark.parametrize(
    "numbers",
    [random.sample(range(1, 1_000), 2) for i in range(100)],
)
def test_stress(numbers):
    assert fast(*numbers) == slow(*numbers)
