import functools
import sys


# Not all subproblems needs to be solved. Recursive should be faster
def recursive(a):
    @functools.lru_cache(maxsize=None)
    def dp(i, v_1, v_2, v_3):
        # Found the partition
        if v_1 == v_2 == v_3 == 0:
            return True

        # No item left
        if i == 0:
            return False

        can_partition = False

        if not can_partition and a[i - 1] <= v_1:
            # Try place i-th item in set 1
            can_partition = dp(i - 1, v_1 - a[i - 1], v_2, v_3)

        if not can_partition and a[i - 1] <= v_2:
            # Try place i-th item in set 2
            can_partition = dp(i - 1, v_1, v_2 - a[i - 1], v_3)

        if not can_partition and a[i - 1] <= v_3:
            # Try place i-th item in set 3
            can_partition = dp(i - 1, v_1, v_2, v_3 - a[i - 1])

        return can_partition

    div, mod = divmod(sum(a), 3)

    return False if mod else dp(len(a), div, div, div)


def iterative(a):
    div, mod = divmod(sum(a), 3)

    if mod:
        return False

    dp = [
        [[[False] * (div + 1) for v_2 in range(div + 1)] for v_1 in range(div + 1)]
        for i in range(len(a) + 1)
    ]

    for i in range(len(a) + 1):
        for v_1 in range(div + 1):
            for v_2 in range(div + 1):
                for v_3 in range(div + 1):
                    if v_1 == v_2 == v_3 == 0:
                        dp[i][v_1][v_2][v_3] = True

                    if not dp[i][v_1][v_2][v_3] and a[i - 1] <= v_1:
                        # Try place i-th item in set 1
                        dp[i][v_1][v_2][v_3] = dp[i - 1][v_1 - a[i - 1]][v_2][v_3]

                    if not dp[i][v_1][v_2][v_3] and a[i - 1] <= v_2:
                        # Try place i-th item in set 2
                        dp[i][v_1][v_2][v_3] = dp[i - 1][v_1][v_2 - a[i - 1]][v_3]

                    if not dp[i][v_1][v_2][v_3] and a[i - 1] <= v_3:
                        # Try place i-th item in set 3
                        dp[i][v_1][v_2][v_3] = dp[i - 1][v_1][v_2][v_3 - a[i - 1]]

    return dp[len(a)][div][div][div]


if __name__ == "__main__":
    n, *A = list(map(int, sys.stdin.read().split()))
    print(int(recursive(A)))
