import math
import sys
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


def distance(p_i, p_j):
    return math.sqrt((p_i.x - p_j.x) ** 2 + (p_i.y - p_j.y) ** 2)


def brute_force(points):
    min_distance = math.inf

    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            p_i, p_j = points[i], points[j]
            dis = (p_i.x - p_j.x) ** 2 + (p_i.y - p_j.y) ** 2
            min_distance = min(min_distance, dis)

    return math.sqrt(min_distance)


def minimum_distance(points):
    x_sorted_points = sorted(points, key=lambda point: point.x)
    y_sorted_points = sorted(points, key=lambda point: point.y)

    return divide_and_conquer(x_sorted_points, y_sorted_points)


def divide_and_conquer(x_sorted_points, y_sorted_points):
    # Base case
    if len(x_sorted_points) <= 3:
        return brute_force(x_sorted_points)

    m = len(x_sorted_points) // 2

    # Divide
    x_left_points = x_sorted_points[:m]
    x_right_points = x_sorted_points[m:]

    x_left_points_set = set(x_left_points)

    y_left_sorted_points = []
    y_right_sorted_points = []

    for point in y_sorted_points:
        if point in x_left_points_set:
            y_left_sorted_points.append(point)
        else:
            y_right_sorted_points.append(point)

    # Conquer
    left_min_distance = divide_and_conquer(x_left_points, y_left_sorted_points)
    right_min_distance = divide_and_conquer(x_right_points, y_right_sorted_points)

    # Combine
    mid_point = x_sorted_points[m]
    d = min(left_min_distance, right_min_distance)

    d_strip_points = []
    for point in y_sorted_points:
        if abs(point.x - mid_point.x) <= d:
            d_strip_points.append(point)

    strip_min_distance = get_strip_min_distance(d_strip_points, d)

    return min(d, strip_min_distance)


def get_strip_min_distance(d_strip_points, d):
    min_distance = d

    for i in range(len(d_strip_points) - 1):
        point_i = d_strip_points[i]

        for j in range(i + 1, len(d_strip_points)):
            point_j = d_strip_points[j]

            # At most 7 points
            if point_j.y - point_i.y < min_distance:
                min_distance = min(min_distance, distance(point_i, point_j))
            else:
                break

    return min_distance


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    xs = data[1::2]
    ys = data[2::2]
    points = [Point(x, y) for x, y in zip(xs, ys)]
    print("{0:.9f}".format(minimum_distance(points)))
