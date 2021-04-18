import functools
import sys
from collections import deque


@functools.lru_cache(maxsize=None)
def recursive(n):
    if n == 0:
        return 0

    min_ops = recursive(n - 1) + 1

    if n % 2 == 0:
        min_ops = min(recursive(n // 2) + 1, min_ops)

    if n % 3 == 0:
        min_ops = min(recursive(n // 3) + 1, min_ops)

    return min_ops


def iterative(n):
    dp = [None] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        dp[i] = dp[i - 1] + 1

        if i % 2 == 0:
            dp[i] = min(dp[i // 2] + 1, dp[i])

        if i % 3 == 0:
            dp[i] = min(dp[i // 3] + 1, dp[i])

    return dp[n]


def iterative_plus(n):
    dp = [None] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        dp[i] = dp[i - 1] + 1

        if i % 2 == 0:
            dp[i] = min(dp[i // 2] + 1, dp[i])

        if i % 3 == 0:
            dp[i] = min(dp[i // 3] + 1, dp[i])

    # Backtrack the dp table
    ops = deque()

    while n >= 1:
        ops.appendleft(n)

        min_ops, new_n = dp[n - 1], n - 1

        if n % 2 == 0 and dp[n // 2] < min_ops:
            min_ops, new_n = dp[n // 2], n // 2

        if n % 3 == 0 and dp[n // 3] < min_ops:
            min_ops, new_n = dp[n // 3], n // 3

        n = new_n

    return list(ops)


if __name__ == "__main__":
    n = int(sys.stdin.read())
    sequence = iterative_plus(n)
    print(len(sequence) - 1)
    for x in sequence:
        print(x, end=" ")
