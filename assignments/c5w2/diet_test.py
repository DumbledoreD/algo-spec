import pytest

from .diet import naive_lin_prog


@pytest.mark.parametrize(
    "A, b, obj, expected",
    [
        (
            [
                [-1, -1],
                [1, 0],
                [0, 1],
            ],
            [-1, 2, 2],
            [-1, 2],
            [0, 2],
        ),
        (
            [
                [1, 1],
                [-1, -1],
            ],
            [1, -2],
            [1, 1],
            None,
        ),
        (
            [
                [0, 0, 1],
            ],
            [3],
            [1, 1, 1],
            float("inf"),
        ),
        (
            [
                [-66, 37],
                [-77, -87],
                [-73, 1],
            ],
            [18658, -15935, 3750],
            [-35, 61],
            float("inf"),
        ),
        (
            [
                [-46, -46, 14],
                [38, -14, -30],
                [23, 100, -86],
            ],
            [-14867, -7071, -10179],
            [100, -30, -80],
            float("inf"),
        ),
    ],
)
def test_basic(A, b, obj, expected):
    assert naive_lin_prog(A, b, obj) == pytest.approx(expected)
