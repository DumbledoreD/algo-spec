import pytest

from .substring_equality import Solver


@pytest.mark.parametrize(
    "text, queries, expected",
    [
        (
            "trololo",
            [(0, 0, 7), (2, 4, 3), (3, 5, 1), (1, 3, 2)],
            [True, True, True, False],
        )
    ],
)
def test_basic(text, queries, expected):
    s = Solver(text)
    assert [s.ask(*query) for query in queries] == expected
