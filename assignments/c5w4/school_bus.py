# Travelling salesman problem

import functools
import sys
from collections import defaultdict
from itertools import combinations


class TravellingSalesmanSolver:
    def __init__(self, graph):
        self.graph = graph

    @property
    def result(self):
        n = len(self.graph)

        # Shortest path from 0 to i, and visits all vertices in set
        prev_size_weight = defaultdict(lambda: float("inf"))
        prev_size_path = defaultdict(lambda: [0])

        for s in self.get_set_of_size(2):
            for i in self.get_vertex_in_set(s):
                prev_size_weight[(s, i)] = self.graph[0][i]
                prev_size_path[(s, i)].append(i)

        for size in range(3, n + 1):
            cur_size_weight = defaultdict(lambda: float("inf"))
            cur_size_path = {}

            for s in self.get_set_of_size(size):

                for i in self.get_vertex_in_set(s):

                    s_p = self.get_set_without_i(s, i)

                    for j in self.get_vertex_in_set(s_p):
                        through_j = prev_size_weight[(s_p, j)] + self.graph[j][i]

                        if through_j < cur_size_weight[(s, i)]:
                            cur_size_weight[(s, i)] = through_j
                            cur_size_path[(s, i)] = prev_size_path[(s_p, j)] + [i]

            prev_size_weight = cur_size_weight
            prev_size_path = cur_size_path

        # Want a cycle, find the min path back to 0
        min_weight = float("inf")
        min_path = None

        all_vertex_set = 2 ** n - 1

        for i in range(1, n):
            through_i = prev_size_weight[(all_vertex_set, i)] + self.graph[i][0]

            if through_i < min_weight:
                min_weight = through_i
                min_path = prev_size_path[(all_vertex_set, i)]

        return min_weight, min_path

    def get_set_of_size(self, size):
        n = len(self.graph)

        # Set has to contain vertex 0, so only choosing (size - 1) vertices
        for combos in combinations(range(1, n), size - 1):
            # Initial 1, as 0-th bit is 1 for vertex 0
            yield functools.reduce(lambda a, b: a + 2 ** b, combos, 1)

    def get_vertex_in_set(self, s):
        binary = bin(s)[2:]

        # Exclude vertex 0, as we can't go back during the path
        for i in range(1, len(self.graph)):
            if i >= len(binary):
                break

            # binary[-2] corresponds to the 1 vertex, etc.
            if binary[len(binary) - i - 1] == "1":
                yield i

    def get_set_without_i(self, s, i):
        # Flip i-th bit
        return s ^ (1 << i)


def build_graph(data):
    nm, *edges = data
    n, _ = map(int, nm.split())

    # Initialize with inf, makes detecting no path easier, also takes care of no edge.
    graph = [[float("inf")] * n for _ in range(n)]

    for edge in edges:
        if edge:
            u, v, weight = map(int, edge.split())
            u -= 1
            v -= 1
            graph[u][v] = graph[v][u] = weight

    return graph


def print_answer(weight, path):
    print(-1 if weight == float("inf") else weight)

    if path:
        print(" ".join(map(str, (i + 1 for i in path))))


if __name__ == "__main__":
    data = sys.stdin.read().split("\n")
    graph = build_graph(data)
    weight, path = TravellingSalesmanSolver(graph).result
    print_answer(weight, path)
