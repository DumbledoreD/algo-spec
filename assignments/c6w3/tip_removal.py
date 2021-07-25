import sys
import threading
from collections import defaultdict, deque


class TipRemover:
    def __init__(self, reads, k):
        self._reads, self._k = reads, k

        self._get_kmers_from_reads()
        self._build_de_bruijn_graph()
        self._build_reverse_graph()
        self._sort_vertices_by_reverse_post_order()
        self._count_sccs()

    def _get_kmers_from_reads(self):
        self._kmers = []

        for read in self._reads:
            if not read:
                continue

            for i in range(len(read) - self._k + 1):
                self._kmers.append(read[i : i + self._k])

    def _build_de_bruijn_graph(self):
        self._de_bruijn_graph = SimpleDeBruijnGraph(self._kmers)

    def _build_reverse_graph(self):
        self._reverse_graph = defaultdict(set)

        for u, vs in self._de_bruijn_graph.adj_list.items():
            for v in vs:
                self._reverse_graph[v].add(u)

    def _sort_vertices_by_reverse_post_order(self):
        self._ordered_vertices = deque()
        self._seen = set()

        for u in self._reverse_graph:
            if u not in self._seen:
                self._dfs(u)

    def _dfs(self, u):
        self._seen.add(u)

        if u in self._reverse_graph:
            for v in self._reverse_graph[u]:
                if v not in self._seen:
                    self._dfs(v)

        self._ordered_vertices.appendleft(u)

    def _count_sccs(self):
        self._scc_count = 0

        self._seen = set()

        for u in self._ordered_vertices:
            if u not in self._seen:
                stack = [u]
                self._seen.add(u)

                while stack:
                    cur_u = stack.pop()

                    for cur_v in self._de_bruijn_graph.adj_list[cur_u]:
                        if cur_v not in self._seen:
                            stack.append(cur_v)
                            self._seen.add(cur_v)

                self._scc_count += 1

    @property
    def result(self):
        return self._scc_count - 1


class SimpleDeBruijnGraph:
    def __init__(self, kmers):
        self._kmers = set(kmers)
        self._build_adj_list()

    def _build_adj_list(self):
        self._adj_list = defaultdict(set)  # Exclude parallel edges

        for kmer in self._kmers:
            left = kmer[:-1]
            right = kmer[1:]

            if left != right:  # Exclude self loops
                self._adj_list[left].add(right)

    @property
    def adj_list(self):
        return self._adj_list

    @property
    def adj_matrix(self):
        # For debugging purpose
        vertices = set()

        for u, vs in self.adj_list.items():
            vertices.add(u)
            vertices.update(vs)

        vertices = sorted(vertices)

        adj_matrix = [[0] * len(vertices) for _ in range(len(vertices))]

        vertex_to_enum = {v: i for i, v in enumerate(vertices)}

        for u, vs in self.adj_list.items():
            for v in vs:
                adj_matrix[vertex_to_enum[u]][vertex_to_enum[v]] = 1

        adj_matrix = "\n".join(",".join(map(str, row)) for row in adj_matrix)

        print(adj_matrix)
        print("\n".join(vertices))


def main():
    reads = sys.stdin.read().split("\n")
    print(TipRemover(reads, 15).result)


if __name__ == "__main__":
    sys.setrecursionlimit(10 ** 7)
    threading.stack_size(2 ** 27)
    threading.Thread(target=main).start()
