import random
import sys


def randomized_quick_sort(a, l, r):
    if l >= r:
        return

    # Random pivot
    pivot = random.randint(l, r)
    a[l], a[pivot] = a[pivot], a[l]

    # Tail recursion elimination
    while l < r:
        m1, m2 = partition3(a, l, r)

        if m1 - l < r - m2:  # left is shorter
            randomized_quick_sort(a, l, m1 - 1)
            l = m2 + 1
        else:
            randomized_quick_sort(a, m2 + 1, r)
            r = m1 - 1

    return a


def partition3(a, l, r):
    pivot = a[l]

    m1 = l
    for i in range(l + 1, r + 1):
        if a[i] < pivot:  # Make left of m1 all smaller than pivot
            m1 += 1
            a[m1], a[i] = a[i], a[m1]

    a[l], a[m1] = a[m1], a[l]

    m2 = m1
    for i in range(m1 + 1, r + 1):
        if a[i] == pivot:  # Make left of m1, right of m2 all equals to the pivot
            m2 += 1
            a[m2], a[i] = a[i], a[m2]

    return m1, m2


def partition2(a, l, r):
    x = a[l]
    j = l
    for i in range(l + 1, r + 1):
        if a[i] <= x:
            j += 1
            a[i], a[j] = a[j], a[i]
    a[l], a[j] = a[j], a[l]
    return j


if __name__ == "__main__":
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    randomized_quick_sort(a, 0, n - 1)
    for x in a:
        print(x, end=" ")
