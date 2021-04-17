import random

import pytest

from .points_and_segments import binary_search as fast


def slow(starts, ends, points):
    cnt = [0] * len(points)
    for i in range(len(points)):
        for j in range(len(starts)):
            if starts[j] <= points[i] <= ends[j]:
                cnt[i] += 1
    return cnt


def gen_segments(starts):
    ends = [s + random.randrange(10) for s in starts]
    return starts, ends


@pytest.mark.parametrize(
    "starts, ends, points",
    [
        (
            *gen_segments([random.randrange(10) for i in range(50)]),
            [random.randrange(20) for i in range(20)],
        )
        for i in range(100)
    ],
)
def test_stress(starts, ends, points):
    assert fast(starts, ends, points) == slow(starts, ends, points)
