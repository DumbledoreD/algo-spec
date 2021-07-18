import sys
import threading
from collections import defaultdict, deque
from functools import reduce
from itertools import islice


class SequenceAssembler:
    def __init__(self, kmers):
        self._path = EulerianCycle(DeBruijnGraph(kmers).edges).result
        self._result = self._remove_border(str(self._path))

    def _remove_border(self, text):
        prefix_function = compute_prefix_function(text)
        return text[prefix_function[-1] :]

    @property
    def result(self):
        return self._result


class DeBruijnGraph:
    def __init__(self, kmers):
        self._kmers = kmers
        self._compute_edges()

    def _compute_edges(self):
        self._edges = []

        for kmer in self._kmers:
            left = kmer[:-1]
            right = kmer[1:]
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


# KMP / Knuth Morris Pratt Algorithm
def compute_prefix_function(text):
    prefix_function = [0] * len(text)
    border_length = 0

    # Iter through prefixes
    for i in range(1, len(text)):
        # border_length is also the index of the char next to the current border
        while border_length > 0 and text[i] != text[border_length]:
            # Retract to the longest border of the current border
            border_length = prefix_function[border_length - 1]

        if text[i] == text[border_length]:
            border_length += 1

        else:
            border_length = 0

        prefix_function[i] = border_length

    return prefix_function


def main():
    kmers = sys.stdin.read().split("\n")
    print(SequenceAssembler(kmers).result)


if __name__ == "__main__":
    sys.setrecursionlimit(10 ** 7)
    threading.stack_size(2 ** 27)
    threading.Thread(target=main).start()
