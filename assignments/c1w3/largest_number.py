import sys
from functools import cmp_to_key


def largest_number(a):
    def compare(m, n):
        m, n = str(m), str(n)
        return int(m + n) - int(n + m)

    a.sort(key=cmp_to_key(compare), reverse=True)
    return "".join(str(d) for d in a)


if __name__ == "__main__":
    data = sys.stdin.read().split()
    a = data[1:]
    print(largest_number(a))
