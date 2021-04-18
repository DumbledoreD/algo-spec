import pytest

from .edit_distance import iterative, recursive


@pytest.mark.parametrize(
    "s, t, expected",
    [
        ("ab", "ab", 0),
        ("short", "ports", 3),
        ("editing", "distance", 5),
    ],
)
def test_basic(s, t, expected):
    assert recursive(s, t) == iterative(s, t) == expected
