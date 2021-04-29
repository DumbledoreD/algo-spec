def build_heap(data):
    """Build a min-heap from ``data`` inplace.

    Returns a sequence of swaps performed by the algorithm.
    """
    swaps = []

    for i in range(len(data) // 2, -1, -1):
        sift_down(i, data, swaps)

    return swaps


def sift_down(i, data, swaps):
    left_child_i, right_child_i = 2 * i + 1, 2 * i + 2

    min_i = i

    if left_child_i < len(data) and data[left_child_i] < data[min_i]:
        min_i = left_child_i

    if right_child_i < len(data) and data[right_child_i] < data[min_i]:
        min_i = right_child_i

    if min_i != i:
        swaps.append((i, min_i))
        data[i], data[min_i] = data[min_i], data[i]
        sift_down(min_i, data, swaps)


def main():
    n = int(input())
    data = list(map(int, input().split()))
    assert len(data) == n

    swaps = build_heap(data)

    print(len(swaps))
    for i, j in swaps:
        print(i, j)


if __name__ == "__main__":
    main()
