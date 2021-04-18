import pytest

from .change_dp import iterative, recuresive


@pytest.mark.parametrize(
    "m",
    list(range(1000)),
)
def test_basic(m):
    assert recuresive(m) == iterative(m)
