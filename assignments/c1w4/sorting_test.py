import random

import pytest

from .sorting import partition3, randomized_quick_sort


@pytest.mark.parametrize(
    "a, expected_a, expected_m1, expected_m2",
    [
        ([1, 2, 3], [1, 2, 3], 0, 0),
        ([2, 1, 3], [1, 2, 3], 1, 1),
        ([3, 1, 2], [2, 1, 3], 2, 2),
        ([1, 1, 2], [1, 1, 2], 0, 1),
        ([2, 2, 1], [1, 2, 2], 1, 2),
        ([3, 1, 3, 4, 1, 5], [1, 1, 3, 3, 4, 5], 2, 3),
    ],
)
def test_partision(a, expected_a, expected_m1, expected_m2):
    m1, m2 = partition3(a, 0, len(a) - 1)
    assert a == expected_a
    assert m1 == expected_m1
    assert m2 == expected_m2


@pytest.mark.parametrize(
    "a", [[random.choice(range(10)) for i in range(10 ** 3)] for i in range(1000)]
)
def test_stress(a):
    assert randomized_quick_sort(a.copy(), 0, len(a) - 1) == sorted(a)
