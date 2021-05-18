import pytest

from .airline_crews import find_bipartite_matching


@pytest.mark.parametrize(
    "u_count, v_count, edges, expected",
    [
        (
            3,
            4,
            [
                (1, 1, 0, 1),
                (0, 1, 0, 0),
                (0, 0, 0, 0),
            ],
            [0, 1, -1],
        ),
        (
            2,
            2,
            [
                (1, 1),
                (1, 0),
            ],
            [1, 0],
        ),
    ],
)
def test_basic(u_count, v_count, edges, expected):
    assert find_bipartite_matching(u_count, v_count, edges) == expected
