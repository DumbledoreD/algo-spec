import sys


def get_majority_element(a, left, right):
    if left == right:
        return a[left]

    middle = (left + right) // 2

    left_maj = get_majority_element(a, left, middle)
    right_maj = get_majority_element(a, middle + 1, right)

    if left_maj == right_maj:
        return left_maj

    left_maj_count = 0
    right_maj_count = 0
    for i in range(left, right + 1):
        left_maj_count += a[i] == left_maj
        right_maj_count += a[i] == right_maj

    maj_count = (right - left + 1) // 2

    return (
        left_maj
        if left_maj_count > maj_count
        else right_maj
        if right_maj_count > maj_count
        else -1
    )


def boyer_moore(a):
    candidate, count = 0, 0

    for num in a:
        if count == 0:
            candidate = num

        count += 1 if num == candidate else -1

    if count == 0:
        return -1

    # Need another scan to confirm the candidate. Consider the case [1, 2, 3]
    maj_count = len(a) // 2
    candidate_count = sum(num == candidate for num in a)

    return candidate if candidate_count > maj_count else -1


if __name__ == "__main__":
    n, *a = list(map(int, sys.stdin.read().split()))
    if get_majority_element(a, 0, n - 1) != -1:
        print(1)
    else:
        print(0)
