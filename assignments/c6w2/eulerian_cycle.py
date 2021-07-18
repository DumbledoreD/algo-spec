# Hierholzer's algo

import sys
import threading
from collections import defaultdict, deque
from itertools import islice


class Path(deque):
    def __str__(self):
        return " ".join(map(str, islice(self, len(self) - 1))) if self else ""


class EulerianCycle:
    def __init__(self, n, edges):
        self._n = n
        self._edges = edges

        self._path = Path()

        is_eulerian = self._build_adj_list()

        if is_eulerian:
            self._find_eulerian_cycle()

    def _build_adj_list(self):
        self._adj_list = defaultdict(list)

        # Vertices are 1-indexed
        in_degrees = [0] * (self._n + 1)
        out_degrees = [0] * (self._n + 1)

        for u, v in self._edges:
            self._adj_list[u].append(v)
            out_degrees[u] += 1
            in_degrees[v] += 1

        # Eulerian cycle iff in-degree == out-degree
        for i in range(1, self._n + 1):
            if in_degrees[i] != out_degrees[i]:
                return False

        return True

    def _find_eulerian_cycle(self):
        self._dfs(1)

    def _dfs(self, cur_node):
        while self._adj_list[cur_node]:
            next_node = self._adj_list[cur_node].pop()
            self._dfs(next_node)

        self._path.appendleft(cur_node)

    @property
    def result(self):
        return self._path


def main():
    nm, *edges = sys.stdin.read().split("\n")
    n, m = map(int, nm.split())
    edges = [tuple(map(int, e.split())) for e in edges if e]
    assert len(edges) == m

    result = EulerianCycle(n, edges).result
    if result:
        print(1, result, sep="\n")
    else:
        print(0)


if __name__ == "__main__":
    sys.setrecursionlimit(10 ** 7)
    threading.stack_size(2 ** 27)
    threading.Thread(target=main).start()
