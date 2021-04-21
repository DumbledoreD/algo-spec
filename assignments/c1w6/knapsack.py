import functools
import sys


def recursive(capacity, weights):
    @functools.lru_cache(maxsize=None)
    def dp(w, i):
        if w == 0 or i == 0:
            return 0

        max_value = dp(w, i - 1)

        if weights[i - 1] <= w:
            max_value = max(max_value, dp(w - weights[i - 1], i - 1) + weights[i - 1])

        return max_value

    return dp(capacity, len(weights))


def iterative(capacity, weights):
    dp = [[None] * (len(weights) + 1) for w in range(capacity + 1)]

    for w in range(capacity + 1):
        for i in range((len(weights) + 1)):
            if w == 0 or i == 0:
                dp[w][i] = 0
            else:
                dp[w][i] = dp[w][i - 1]

                if weights[i - 1] <= w:
                    dp[w][i] = max(
                        dp[w][i], dp[w - weights[i - 1]][i - 1] + weights[i - 1]
                    )

    return dp[capacity][len(weights)]


if __name__ == "__main__":
    W, n, *w = list(map(int, sys.stdin.read().split()))
    print(iterative(W, w))
