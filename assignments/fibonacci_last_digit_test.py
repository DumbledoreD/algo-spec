import pytest

from .fibonacci_last_digit import get_fibonacci_last_digit as fast


def slow(n):
    if n <= 1:
        return n

    previous = 0
    current = 1

    for _ in range(n - 1):
        previous, current = current, previous + current

    return current % 10


@pytest.mark.parametrize("n", range(100))
def test_basic(n):
    assert fast(n) == slow(n)
