import pytest

from .fibonacci import calc_fib as fast


def slow(n):
    if n <= 1:
        return n

    return slow(n - 1) + slow(n - 2)


@pytest.mark.parametrize("n", range(30))
def test_basic(n):
    assert fast(n) == slow(n)
