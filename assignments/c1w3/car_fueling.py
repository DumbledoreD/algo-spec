# python3
import sys


def compute_min_refills(distance, tank, stops):
    stops = stops + [distance]
    remaining_fuel = tank
    i, refills = -1, 0

    while i < len(stops) - 1:
        dis_to_next_stop = stops[0] if i == -1 else stops[i + 1] - stops[i]

        # Next stop not attainbale
        if dis_to_next_stop > tank:
            return -1

        # Move to the next top
        if dis_to_next_stop <= remaining_fuel:
            remaining_fuel -= dis_to_next_stop
            i += 1

        # Refill at the current stop
        else:
            refills += 1
            remaining_fuel = tank

    return refills


if __name__ == "__main__":
    d, m, _, *stops = map(int, sys.stdin.read().split())
    print(compute_min_refills(d, m, stops))
