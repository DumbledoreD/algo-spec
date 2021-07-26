import sys
from collections import defaultdict
from itertools import combinations


class BubbleDetector:
    def __init__(self, reads, k, t):
        self._reads, self._k, self._t = reads, k, t

        self._get_kmers_from_reads()
        self._build_de_bruijn_graph()
        self._get_multi_out_path_nodes()
        self._get_multi_in_path_nodes()
        self._build_start_to_end_node_paths()
        self._count_bubbles()

    def _get_kmers_from_reads(self):
        self._kmers = []

        for read in self._reads:
            if not read:
                continue

            for i in range(len(read) - self._k + 1):
                self._kmers.append(read[i : i + self._k])

    def _build_de_bruijn_graph(self):
        self._de_bruijn_graph = SimpleDeBruijnGraph(self._kmers)

    def _get_multi_out_path_nodes(self):
        self._start_nodes = []

        for node, outs in self._de_bruijn_graph.adj_list.items():
            if len(outs) > 1:
                self._start_nodes.append(node)

    def _get_multi_in_path_nodes(self):
        self._end_nodes = set()

        seen = set()

        for outs in self._de_bruijn_graph.adj_list.values():
            for node in outs:
                if node in seen:
                    self._end_nodes.add(node)
                else:
                    seen.add(node)

    def _build_start_to_end_node_paths(self):
        self._start_to_end_paths = defaultdict(list)

        for start_node in self._start_nodes:
            self._dfs(start_node)

    def _dfs(self, start_node):
        stack = [(start_node, set())]

        while stack:
            u, path = stack.pop()

            for v in self._de_bruijn_graph.adj_list[u]:
                # Note: need all paths, not just a paht.
                # Thus check `v in path`, not `v in seen`.
                if v in path or v == start_node:
                    continue

                if v in self._end_nodes:
                    self._start_to_end_paths[(start_node, v)].append(path)

                if len(path) + 1 < self._t:
                    new_path = path | set([v])
                    stack.append((v, new_path))

    def _count_bubbles(self):
        self._count = 0

        for paths in self._start_to_end_paths.values():
            if len(paths) < 2:
                continue

            for p1, p2 in combinations(paths, 2):
                if not (p1 & p2):  # Disjoint paths
                    self._count += 1
                    continue

    @property
    def result(self):
        return self._count


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
    (kt, *reads) = sys.stdin.read().split("\n")
    k, t = map(int, kt.split())
    print(BubbleDetector(reads, k, t).result)


if __name__ == "__main__":
    main()
