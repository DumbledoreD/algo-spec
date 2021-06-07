import sys


class GraphColorSolver:
    def __init__(self, colors):
        self.colors = colors

    def get_cnfs(self, n, edges):
        self._reset()
        self._get_var_count(n)
        self._add_cnf_for_vertex(n)
        self._add_cnf_for_edges(edges)
        return self._var_count, self._cnfs

    def _reset(self):
        self._var_count = 0
        self._cnfs = []

    def _get_var_count(self, n):
        # A separate variable x_i_j for each vertex i of the initial graph and each
        # possible color j
        self._var_count = n * self.colors

    def _add_cnf_for_vertex(self, n):
        # Each vertex has to be colored by some color, (vertices use 1-based index)
        for i in range(1, n + 1):
            var_index = (i - 1) * self.colors + 1
            # (x_i_1 v x_i_2 v ... x_i_j)
            self._cnfs.append(" ".join(str(var_index + j) for j in range(self.colors)))

    def _add_cnf_for_edges(self, edges):
        # Vertices connected by an edge must have different colors
        for u, v in edges:
            u_index = (u - 1) * self.colors + 1
            v_index = (v - 1) * self.colors + 1

            for j in range(self.colors):
                # Not both, (-x_u_j v -x_v_j)
                self._cnfs.append(" ".join([str(-(u_index + j)), str(-(v_index + j))]))


if __name__ == "__main__":
    inputs = sys.stdin.read().split("\n")
    n, m = map(int, inputs[0].split())
    edges = [tuple(map(int, edge.split())) for edge in inputs[1:] if edge]

    solver = GraphColorSolver(3)
    var_count, cnfs = solver.get_cnfs(n, edges)

    print(len(cnfs), var_count)

    for cnf in cnfs:
        print(cnf + " 0")
