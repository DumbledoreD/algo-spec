import pytest

from .change_dp import iterative, recursive


@pytest.mark.parametrize("m", list(range(1000)))
def test_basic(m):
    assert recursive(m) == iterative(m)
