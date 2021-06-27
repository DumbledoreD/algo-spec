# 3-recoloring => 2-SAT

import sys
import threading
from collections import deque
from itertools import combinations

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10 ** 6)  # max depth of recursion
threading.stack_size(2 ** 26)  # new thread will get stack of such size


class ThreeColorSolver:
    def __init__(self, initial_colors, edges):
        self.reducer = ThreeColorToTwoSatisfiabilityReducer(initial_colors, edges)
        self.solver = TwoSatisfiabilitySolver(
            self.reducer.var_count, self.reducer.clauses
        )

    @property
    def result(self):
        return self.reducer.convert_assignment_to_colors(self.solver.result)


class ThreeColorToTwoSatisfiabilityReducer:
    COLORS = "RGB"

    def __init__(self, initial_colors, edges):
        self._initial_colors = initial_colors
        self._edges = edges

        self._clauses = []
        self._add_vertex_clauses()
        self._add_edge_clauses()

    @property
    def var_count(self):
        return len(self._initial_colors) * len(self.COLORS)

    @property
    def clauses(self):
        return self._clauses

    def _add_vertex_clauses(self):
        # Vars are 1-indexed
        for v, color in enumerate(self._initial_colors, 1):
            initial_color_var = self._get_var(v, color)

            # Can't pick the initial color
            self._clauses.append(
                [var for var in self._get_vars(v) if var != initial_color_var]
            )

            # Can only pick 1 color per vertex
            for i, j in combinations(self._get_vars(v), 2):
                self._clauses.append([-i, -j])

    def _add_edge_clauses(self):
        for u, v in self._edges:
            # Can't be the same color
            for color in self.COLORS:
                u_var = self._get_var(u, color)
                v_var = self._get_var(v, color)
                self._clauses.append([-u_var, -v_var])

    def _get_var(self, v, color):
        # Vars are 1-indexed
        return (v - 1) * 3 + self.COLORS.find(color) + 1

    def _get_vars(self, v):
        # Vars are 1-indexed
        for i in range(len(self.COLORS)):
            yield (v - 1) * len(self.COLORS) + i + 1

    def convert_assignment_to_colors(self, assignment):
        if not assignment:
            return None

        return "".join(self.COLORS[(v - 1) % 3] for v in assignment if v > 0)


class TwoSatisfiabilitySolver:
    def __init__(self, var_count, clauses):
        self.var_count = var_count
        self.clauses = clauses

        self.build_implication_graph()
        self.build_reverse_graph()
        self.get_top_order_on_reverse_graph()
        self.build_assignment()

    def build_implication_graph(self):
        # Vars are 1-indexed
        self.graph = [[] for _ in range(self.var_count * 2 + 1)]

        for l1, l2 in self.clauses:
            self.graph[-l1].append(l2)
            self.graph[-l2].append(l1)

    def build_reverse_graph(self):
        # Vars are 1-indexed
        self.reverse_graph = [[] for _ in range(self.var_count * 2 + 1)]

        for i, js in enumerate(self.graph):
            if i:  # Vars are 1-indexed
                for j in js:
                    self.reverse_graph[j].append(i)

    def get_top_order_on_reverse_graph(self):
        # Vars are 1-indexed
        self.seen = [False] * (self.var_count * 2 + 1)
        self.order = deque()

        for v in range(1, self.var_count + 1):
            if not self.seen[v]:
                self.dfs_on_reverse_graph(v)

            if not self.seen[-v]:
                self.dfs_on_reverse_graph(-v)

    def dfs_on_reverse_graph(self, v):
        self.seen[v] = True

        for next_v in self.reverse_graph[v]:
            if not self.seen[next_v]:
                self.dfs_on_reverse_graph(next_v)

        # Append on the post order
        self.order.appendleft(v)

    def build_assignment(self):
        # Vars are 1-indexed
        seen = [False] * (self.var_count * 2 + 1)
        self.assignment = [None] * (self.var_count * 2 + 1)

        # Top order on the reverse graph == reverse top order on the implication graph
        for v in self.order:
            if not seen[v]:
                stack = [v]
                scc = set()

                seen[v] = True
                scc.add(v)

                while stack:
                    cur_v = stack.pop()

                    # If both v and its negation in the same SCC => unsatisfiable
                    if -cur_v in scc:
                        self.assignment = None
                        return

                    # If unassigned, assign literal to 1 and negation to 0
                    if self.assignment[cur_v] is None:
                        self.assignment[cur_v] = 1
                        self.assignment[-cur_v] = 0

                    for next_v in self.graph[cur_v]:
                        if not seen[next_v]:
                            stack.append(next_v)
                            seen[next_v] = True
                            scc.add(next_v)

    @property
    def result(self):
        return (
            [v if self.assignment[v] else -v for v in range(1, self.var_count + 1)]
            if self.assignment
            else None
        )


def print_answer(assignment):
    print(assignment if assignment else "Impossible")


def main():
    data = sys.stdin.read().split("\n")
    _, initial_colors, *edges = data
    edges = [list(map(int, edge.split())) for edge in edges if edge]
    assignment = ThreeColorSolver(initial_colors, edges).result
    print_answer(assignment)


if __name__ == "__main__":
    # This is to avoid stack overflow issues
    threading.Thread(target=main).start()
