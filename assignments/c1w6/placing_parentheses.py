import functools
from operator import add, mul, sub

OPS = {"+": add, "-": sub, "*": mul}


def recursive(digits, operators):
    @functools.lru_cache(maxsize=None)
    def dp(i, j):
        if i == j:
            return int(digits[i]), int(digits[i])

        min_val, max_val = float("inf"), -float("inf")

        for k in range(i, j):
            left_min, left_max = dp(i, k)
            right_min, right_max = dp(k + 1, j)

            op = OPS[operators[k]]

            min_val = min(
                min_val,
                op(left_min, right_min),
                op(left_min, right_max),
                op(left_max, right_min),
                op(left_max, right_max),
            )

            max_val = max(
                max_val,
                op(left_min, right_min),
                op(left_min, right_max),
                op(left_max, right_min),
                op(left_max, right_max),
            )

        return min_val, max_val

    return dp(0, len(digits) - 1)


def iterative(digits, operators):
    min_values = [[None] * len(digits) for i in range(len(digits))]
    max_values = [[None] * len(digits) for i in range(len(digits))]

    for d in range(len(digits)):
        for i in range(len(digits) - d):
            if d == 0:
                min_values[i][i] = max_values[i][i] = int(digits[i])
            else:
                j = i + d

                min_val, max_val = float("inf"), -float("inf")

                for k in range(i, j):
                    left_min, left_max = min_values[i][k], max_values[i][k]
                    right_min, right_max = min_values[k + 1][j], max_values[k + 1][j]

                    op = OPS[operators[k]]

                    min_val = min(
                        min_val,
                        op(left_min, right_min),
                        op(left_min, right_max),
                        op(left_max, right_min),
                        op(left_max, right_max),
                    )

                    max_val = max(
                        max_val,
                        op(left_min, right_min),
                        op(left_min, right_max),
                        op(left_max, right_min),
                        op(left_max, right_max),
                    )

                min_values[i][j], max_values[i][j] = min_val, max_val

    return min_values[i][len(digits) - 1], max_values[i][len(digits) - 1]


def get_maximum_value(expression):
    digits, operators = expression[::2], expression[1::2]
    _, max_val = iterative(digits, operators)
    return max_val


if __name__ == "__main__":
    print(get_maximum_value(input()))
