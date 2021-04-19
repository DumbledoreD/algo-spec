import functools
import sys


def recursive(a, b, c):
    @functools.lru_cache(maxsize=None)
    def dp(i, j, k):
        if i == 0 or j == 0 or k == 0:
            return 0

        if a[i - 1] == b[j - 1] == c[k - 1]:
            return dp(i - 1, j - 1, k - 1) + 1

        else:
            return max(
                dp(i - 1, j, k),
                dp(i, j - 1, k),
                dp(i, j, k - 1),
            )

    return dp(len(a), len(b), len(c))


def iterative(a, b, c):
    dp = [[[None] * (len(c) + 1) for j in range(len(b) + 1)] for i in range(len(a) + 1)]

    for i in range(len(a) + 1):
        for j in range(len(b) + 1):
            for k in range(len(c) + 1):
                if i == 0 or j == 0 or k == 0:
                    dp[i][j][k] = 0

                elif a[i - 1] == b[j - 1] == c[k - 1]:
                    dp[i][j][k] = dp[i - 1][j - 1][k - 1] + 1

                else:
                    dp[i][j][k] = max(
                        dp[i - 1][j][k],
                        dp[i][j - 1][k],
                        dp[i][j][k - 1],
                    )

    return dp[len(a)][len(b)][len(c)]


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    an = data[0]
    data = data[1:]
    a = data[:an]
    data = data[an:]
    bn = data[0]
    data = data[1:]
    b = data[:bn]
    data = data[bn:]
    cn = data[0]
    data = data[1:]
    c = data[:cn]
    print(iterative(a, b, c))
