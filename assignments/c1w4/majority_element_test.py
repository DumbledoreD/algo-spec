from collections import Counter

import pytest

from .majority_element import boyer_moore, get_majority_element


def cheat(a):
    counter = Counter(a)
    num, count = counter.most_common(1)[0]
    return num if count > len(a) // 2 else -1


@pytest.mark.parametrize(
    "a, expected",
    [
        ([1], 1),
        ([1, 1], 1),
        ([1, 2], -1),
        ([1, 1, 2], 1),
        ([1, 2, 2], 2),
        ([1, 2, 1], 1),
        ([1, 2, 3], -1),
    ],
)
def test_basic(a, expected):
    assert get_majority_element(a, 0, len(a) - 1) == boyer_moore(a) == expected
