import pytest

from .evacuation import build_adjacency_matrix, ford_fulkerson


@pytest.mark.parametrize(
    "node_count, edges, expected",
    [
        (
            5,
            [
                (0, 1, 2),
                (1, 4, 5),
                (0, 2, 6),
                (2, 3, 2),
                (3, 4, 1),
                (2, 1, 3),
                (1, 3, 1),
            ],
            6,
        )
    ],
)
def test_basic(node_count, edges, expected):
    adj_matrix = build_adjacency_matrix(node_count, edges)
    assert ford_fulkerson(adj_matrix, source=0, sink=node_count - 1) == expected
