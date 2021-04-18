import functools


def recursive(s, t):
    @functools.lru_cache(maxsize=None)
    def dp(i, j):
        if i == 0 or j == 0:
            return i or j

        return min(
            dp(i, j - 1) + 1,  # insertion
            dp(i - 1, j) + 1,  # deletion
            dp(i - 1, j - 1) + int(s[i - 1] != t[j - 1]),  # match/mismatch
        )

    return dp(len(s), len(t))


def iterative(s, t):
    dp = [[None] * (len(t) + 1) for row in range((len(s) + 1))]

    for i in range(len(s) + 1):
        for j in range(len(t) + 1):
            if i == 0 or j == 0:
                dp[i][j] = i or j
            else:
                dp[i][j] = min(
                    dp[i][j - 1] + 1,
                    dp[i - 1][j] + 1,
                    dp[i - 1][j - 1] + int(s[i - 1] != t[j - 1]),
                )

    return dp[-1][-1]


if __name__ == "__main__":
    print(iterative(input(), input()))
