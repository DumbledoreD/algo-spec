import pytest

from .common_substring import Solver, SolverV2


@pytest.mark.parametrize(
    "s, t, expected",
    [
        ("aaa", "bbb", (0, 0, 0)),
        ("ssstt", "ttsss", (0, 2, 3)),
        ("aabcd", "fghaa", (0, 3, 2)),
        ("aaa", "aaa", (0, 0, 3)),
    ],
)
def test_basic(s, t, expected):
    assert (
        Solver(s, t).longest_common_substring()
        == SolverV2(s, t).longest_common_substring()
        == expected
    )
