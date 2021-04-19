import functools
import sys


def recursive(a, b):
    @functools.lru_cache(maxsize=None)
    def dp(i, j):
        if i == 0 or j == 0:
            return 0

        if a[i - 1] == b[j - 1]:
            return dp(i - 1, j - 1) + 1

        else:
            return max(dp(i - 1, j), dp(i, j - 1))

    return dp(len(a), len(b))


def iterative(a, b):
    dp = [[None] * (len(b) + 1) for row in range((len(a) + 1))]

    for i in range(len(a) + 1):
        for j in range(len(b) + 1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[len(a)][len(b)]


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))

    n = data[0]
    data = data[1:]
    a = data[:n]

    data = data[n:]
    m = data[0]
    data = data[1:]
    b = data[:m]

    print(iterative(a, b))
