import random

import pytest

from .inversions import get_number_of_inversions, merge_sort


@pytest.mark.parametrize(
    "a", [[random.choice(range(10)) for i in range(10 ** 3)] for i in range(1000)]
)
def test_stress(a):
    assert merge_sort(a.copy()) == sorted(a)


@pytest.mark.parametrize(
    "a, expected",
    [
        ([6, 5, 4, 3, 2, 1], 6 * 5 / 2),
        ([1, 2, 3, 4, 5], 0),
        ([2, 3, 9, 2, 9], 2),
    ],
)
def test_basic(a, expected):
    assert get_number_of_inversions(a) == expected
