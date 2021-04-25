import random

import pytest

from .max_sliding_window import max_sliding_window as fast
from .max_sliding_window import max_sliding_window_naive as slow


@pytest.mark.parametrize(
    "sequence, m, expected",
    [
        ([1, 2, 3, 4, 5], 3, [3, 4, 5]),
        ([5, 4, 3, 2, 1], 3, [5, 4, 3]),
        ([1, 1, 1, 2, 2], 3, [1, 2, 2]),
        ([2, 2, 2, 1, 1, 1], 3, [2, 2, 2, 1]),
    ],
)
def test_basic(sequence, m, expected):
    assert fast(sequence, m) == expected


@pytest.mark.parametrize(
    "sequence, m",
    [
        ([random.randrange(10) for _ in range(20)], random.randint(1, 5))
        for t in range(1000)
    ],
)
def test_stress(sequence, m):
    assert fast(sequence, m) == slow(sequence, m)
