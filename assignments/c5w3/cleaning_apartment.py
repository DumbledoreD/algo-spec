import collections
import itertools
import sys


class HamiltonCycleSolver:
    def get_cnfs(self, n, edges):
        self._reset(n, edges)

        self._get_var_count()
        self._add_constr_1()
        self._add_constr_2()
        self._add_constr_3()
        self._add_constr_4()
        self._add_constr_5()

        return self._var_count, self._cnfs

    def _reset(self, n, edges):
        self.n, self.edges = n, edges
        self._var_count = 0
        self._cnfs = []

    def _get_var_count(self):
        # A separate variable x_i_j for each vertex i and each position j in the
        # Hamiltonian path.
        self._var_count = self.n * self.n

    def _var(self, i=None, j=None):
        # Both i and j use 1-based index

        # All positions var for vertex i
        if i and not j:
            start = (i - 1) * self.n + 1
            return range(start, start + self.n)

        # All vertices var for position j
        if not i and j:
            return range(j, self._var_count + 1, self.n)

        # Var for vertex i and position j
        if i and j:
            return (i - 1) * self.n + j

        raise Exception()

    def _add_constr_1(self):
        # Each vertex has to take a position on the path.
        for i in range(1, self.n + 1):
            vars_for_vertex_i = self._var(i=i)
            cnf = " ".join(map(str, vars_for_vertex_i))
            self._cnfs.append(cnf)

    def _add_constr_2(self):
        # Each vertex appears just once in a path (redundant but speeds up the solver).
        for i in range(1, self.n + 1):
            vars_for_vertex_i = self._var(i=i)
            for combos in itertools.combinations(vars_for_vertex_i, 2):
                cnf = " ".join(str(-var) for var in combos)
                self._cnfs.append(cnf)

    def _add_constr_3(self):
        # Each position in a path is occupied by some vertex.
        for j in range(1, self.n + 1):
            vars_for_position_j = self._var(j=j)
            cnf = " ".join(map(str, vars_for_position_j))
            self._cnfs.append(cnf)

    def _add_constr_4(self):
        # No two vertices occupy the same position of a path.
        for j in range(1, self.n + 1):
            vars_for_position_j = self._var(j=j)
            for combos in itertools.combinations(vars_for_position_j, 2):
                cnf = " ".join(str(-var) for var in combos)
                self._cnfs.append(cnf)

    def _add_constr_5(self):
        # Two successive vertices on a path must be connected by an edge.
        graph = self._build_graph(edges)

        for u, v in itertools.combinations(range(1, self.n + 1), 2):
            if v not in graph[u]:
                for j in range(1, self.n):
                    # Can't have both x_u_j and x_v_(j+1) be True
                    var_u = self._var(u, j)
                    var_v = self._var(v, j + 1)
                    cnf = " ".join([str(-var_u), str(-var_v)])
                    self._cnfs.append(cnf)

                    # Can't have both x_v_j and x_u_(j+1) be True
                    var_u = self._var(u, j + 1)
                    var_v = self._var(v, j)
                    cnf = " ".join([str(-var_u), str(-var_v)])
                    self._cnfs.append(cnf)

    def _build_graph(self, edges):
        graph = collections.defaultdict(set)

        for u, v in edges:
            graph[u].add(v)
            graph[v].add(u)

        return graph


if __name__ == "__main__":
    inputs = sys.stdin.read().split("\n")
    n, m = map(int, inputs[0].split())
    edges = [tuple(map(int, edge.split())) for edge in inputs[1:] if edge]

    solver = HamiltonCycleSolver()
    var_count, cnfs = solver.get_cnfs(n, edges)

    print(len(cnfs), var_count)

    for cnf in cnfs:
        print(cnf + " 0")
