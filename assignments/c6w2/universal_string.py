import sys
import threading
from collections import defaultdict, deque
from functools import reduce
from itertools import islice


class DeBruijnGraph:
    def __init__(self, k):
        self._k = k
        self._compute_edges()

    def _compute_edges(self):
        self._edges = []

        for i in range(2 ** self._k):
            binary = "{:b}".format(i).rjust(self._k, "0")
            left = binary[:-1]
            right = binary[1:]
            self._edges.append((left, right))

    @property
    def edges(self):
        return self._edges


class Path(deque):
    def __str__(self):
        return reduce(
            lambda a, x: a[: -len(x) + 1] + x,
            map(str, islice(self, len(self) - 1)),
            "",
        )


class EulerianCycle:
    def __init__(self, edges):
        self._edges = edges

        self._path = Path()

        is_eulerian = self._build_adj_list()

        if is_eulerian:
            self._dfs(self._edges[0][0])

    def _build_adj_list(self):
        self._adj_list = defaultdict(list)

        in_degrees = defaultdict(int)
        out_degrees = defaultdict(int)

        for u, v in self._edges:
            self._adj_list[u].append(v)
            out_degrees[u] += 1
            in_degrees[v] += 1

        # Eulerian cycle iff in-degree == out-degree
        for key in self._adj_list:
            if in_degrees[key] != out_degrees[key]:
                return False

        return True

    def _dfs(self, cur_node):
        while self._adj_list[cur_node]:
            next_node = self._adj_list[cur_node].pop()
            self._dfs(next_node)

        self._path.appendleft(cur_node)

    @property
    def result(self):
        return self._path


def main():
    k = int(sys.stdin.read())
    print(EulerianCycle(DeBruijnGraph(k).edges).result)


if __name__ == "__main__":
    sys.setrecursionlimit(10 ** 7)
    threading.stack_size(2 ** 27)
    threading.Thread(target=main).start()
