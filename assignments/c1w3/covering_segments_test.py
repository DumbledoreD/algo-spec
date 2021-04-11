import pytest

from .covering_segments import Segment, optimal_points


@pytest.mark.parametrize(
    "segments, expected",
    [
        pytest.param([Segment(0, 1)], [1], id="one segment"),
        pytest.param([Segment(0, 0), Segment(0, 0)], [0], id="boundary"),
        pytest.param([Segment(0, 1), Segment(1, 2)], [1], id="simple"),
        pytest.param(
            [Segment(0, 1), Segment(1, 3), Segment(2, 5), Segment(3, 6), Segment(4, 7)],
            [1, 5],
            id="general",
        ),
    ],
)
def test_basic(segments, expected):
    assert optimal_points(segments) == expected
