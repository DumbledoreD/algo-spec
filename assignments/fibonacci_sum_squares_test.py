import pytest

from .fibonacci_sum_squares import fibonacci_sum_squares as fast


def slow(n):
    if n <= 1:
        return n

    previous = 0
    current = 1
    fib_sum = 1

    for _ in range(n - 1):
        previous, current = current, previous + current
        fib_sum += current * current

    return fib_sum % 10


@pytest.mark.parametrize("n", range(1000))
def test_basic(n):
    assert fast(n) == slow(n)


def test_large_num():
    assert fast(10 ** 14)
