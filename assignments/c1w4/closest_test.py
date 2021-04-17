import random

import pytest

from .closest import Point
from .closest import brute_force as slow
from .closest import minimum_distance as fast


@pytest.mark.parametrize(
    "xs, ys",
    [
        (
            [random.randrange(100) for x in range(25)],
            [random.randrange(100) for y in range(25)],
        )
        for case in range(1000)
    ],
)
def test_stress(xs, ys):
    points = [Point(x, y) for x, y in zip(xs, ys)]
    assert fast(points) == slow(points)
