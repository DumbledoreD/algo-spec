import pytest

from .tree_height import compute_height


@pytest.mark.parametrize(
    "parents, expected",
    [
        ([-1], 1),
        ([-1, 0, 0], 2),
        ([-1, 0, 0, 1], 3),
        ([-1, 0, 1, 2], 4),
    ],
)
def test_basic(parents, expected):
    assert compute_height(parents) == expected
