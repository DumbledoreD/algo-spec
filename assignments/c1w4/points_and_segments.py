import bisect
import sys


def binary_search(starts, ends, points):
    starts, ends = sorted(starts), sorted(ends)
    seg_count = len(starts)
    result = []

    for point in points:
        ends_before = bisect.bisect_left(ends, point)
        starts_after = seg_count - bisect.bisect_right(starts, point)
        result.append(seg_count - ends_before - starts_after)

    return result


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    m = data[1]
    starts = data[2 : 2 * n + 2 : 2]
    ends = data[3 : 2 * n + 2 : 2]
    points = data[2 * n + 2 :]
    cnt = binary_search(starts, ends, points)
    for x in cnt:
        print(x, end=" ")
