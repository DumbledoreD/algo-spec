import sys


def get_optimal_value(capacity, weights, values):
    values_per_unit_weight = [(v / w, w) for v, w in zip(values, weights)]
    values_per_unit_weight.sort()

    total_value = 0.0

    while capacity and values_per_unit_weight:
        v_per_w, w = values_per_unit_weight.pop()
        total_value += v_per_w * min(w, capacity)
        capacity -= min(w, capacity)

    return total_value


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, capacity = data[0:2]
    values = data[2 : (2 * n + 2) : 2]
    weights = data[3 : (2 * n + 2) : 2]
    opt_value = get_optimal_value(capacity, weights, values)
    print("{:.10f}".format(opt_value))
