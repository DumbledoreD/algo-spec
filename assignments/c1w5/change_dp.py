import functools
import sys

coins = [1, 3, 4]


@functools.lru_cache(maxsize=None)
def recuresive(m):
    if m == 0:
        return 0

    min_change = float("inf")
    for c in coins:
        if c <= m:
            min_change = min(recuresive(m - c) + 1, min_change)

    return min_change


def iterative(m):
    dp = [float("inf")] * (m + 1)
    dp[0] = 0

    for i in range(1, m + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i - c] + 1, dp[i])

    return dp[m]


if __name__ == "__main__":
    m = int(sys.stdin.read())
    print(iterative(m))
