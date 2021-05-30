import pytest

from .energy_values import naive_gaussian_elimination


@pytest.mark.parametrize(
    "augmented_matrix, expected",
    [
        (
            [
                [1, 0, 0, 0, 1],
                [0, 1, 0, 0, 2],
                [0, 0, 1, 0, 3],
                [0, 0, 0, 1, 4],
            ],
            [1, 2, 3, 4],
        ),
        (
            [
                [5, -5, -1],
                [-1, -2, -1],
            ],
            [0.2, 0.4],
        ),
    ],
)
def test_basic(augmented_matrix, expected):
    assert naive_gaussian_elimination(augmented_matrix) == pytest.approx(expected)
