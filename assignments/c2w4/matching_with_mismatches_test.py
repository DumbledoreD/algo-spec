import pytest

from .matching_with_mismatches import Solver


@pytest.mark.parametrize(
    "k, text, pattern, expected",
    [
        (0, "ababab", "baaa", []),
        (1, "ababab", "baaa", [1]),
        (1, "xabcabc", "ccc", []),
        (2, "xabcabc", "ccc", [1, 2, 3, 4]),
        (3, "aaa", "xxx", [0]),
    ],
)
def test_basic(k, text, pattern, expected):
    assert Solver(k, text, pattern).matches() == expected
