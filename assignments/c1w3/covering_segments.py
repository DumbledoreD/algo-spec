import sys
from collections import namedtuple

Segment = namedtuple("Segment", "start end")


def optimal_points(segments):
    segments.sort(key=lambda segment: segment.end)
    points = []
    cur_min_end = -1

    for segment in segments:
        if segment.start > cur_min_end:
            cur_min_end = segment.end
            points.append(cur_min_end)

    return points


if __name__ == "__main__":
    n, *data = map(int, sys.stdin.read().split())
    segments = list(map(lambda x: Segment(x[0], x[1]), zip(data[::2], data[1::2])))
    points = optimal_points(segments)
    print(len(points))
    print(*points)
