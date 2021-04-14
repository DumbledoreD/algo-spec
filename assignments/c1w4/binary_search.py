import sys


def binary_search(a, x):
    l, r = 0, len(a) - 1

    while l <= r:
        m = (l + r) // 2

        if a[m] == x:
            return m

        if a[m] > x:  # First half
            r = m - 1

        else:  # Second half
            l = m + 1

    return -1


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    m = data[n + 1]
    a = data[1 : n + 1]
    for x in data[n + 2 :]:
        print(binary_search(a, x), end=" ")
