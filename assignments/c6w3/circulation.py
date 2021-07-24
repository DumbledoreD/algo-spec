import sys
from enum import Enum
from itertools import chain


class FlowDirection(Enum):
    Forward = 0
    Backward = 1


class FordFulkersonWithLowerBound:
    def __init__(self, n, edges):
        graph = GraphBuilder(n, edges)
        self._vertices, self._edges = graph.vertices, graph.edges

        self._remove_lower_bound()
        self._add_super_nodes()
        self._do_ford_fulkerson()
        self._restore_lower_bound()

    def _remove_lower_bound(self):
        for edge in self._edges:
            edge.ub -= edge.lb

            # dv' = dv - (Lin - Lout)
            # dv - original vertex demand
            # Lin - sum of vertex input edges lower bounds
            # Lout - sum of vertex output edges lower bounds
            edge.fr.demand += edge.lb
            edge.to.demand -= edge.lb

    def _add_super_nodes(self):
        self._super_source = Vertex("source")
        self._super_sink = Vertex("sink")
        self._total_demand = 0

        for vertex in self._vertices:
            if vertex.demand < 0:
                self._super_source.outs.append(
                    Edge(0, -vertex.demand, self._super_source, vertex)
                )

            elif vertex.demand > 0:
                vertex.outs.append(Edge(0, vertex.demand, vertex, self._super_sink))
                self._total_demand += vertex.demand

    def _do_ford_fulkerson(self):
        self._max_flow = 0

        while True:
            path = self._dfs()

            if not path:
                break

            # Find the min flow in the path
            path_flow = float("inf")

            for direction, edge in path:
                if direction == FlowDirection.Forward:
                    path_flow = min(path_flow, edge.ub - edge.flow)

                elif direction == FlowDirection.Backward:
                    path_flow = min(path_flow, edge.flow)

            # Update the flow along the path
            for direction, edge in path:
                if direction == FlowDirection.Forward:
                    edge.flow += path_flow

                elif direction == FlowDirection.Backward:
                    edge.flow -= path_flow

            self._max_flow += path_flow

    def _dfs(self):
        seen = set()
        seen.add(self._super_source)

        stack = [(self._super_source, [])]

        while stack:
            u, path = stack.pop()

            for edge in chain(u.outs, u.ins):
                if edge.fr == u and edge.flow < edge.ub:
                    direction = FlowDirection.Forward
                    next_node = edge.to

                elif edge.to == u and edge.flow != 0:
                    direction = FlowDirection.Backward
                    next_node = edge.fr

                else:
                    continue

                if next_node in seen:
                    continue

                new_path = path + [(direction, edge)]

                if next_node == self._super_sink:
                    return new_path

                stack.append((next_node, new_path))
                seen.add(next_node)

    def _restore_lower_bound(self):
        for edge in self._edges:
            edge.flow += edge.lb
            edge.ub += edge.lb

            edge.fr.demand -= edge.lb
            edge.to.demand += edge.lb

    @property
    def solvable(self):
        return self._max_flow == self._total_demand

    @property
    def edges(self):
        return self._edges


class GraphBuilder:
    def __init__(self, n, edges):
        self._build_vertices(n)
        self._build_edges(edges)

    def _build_vertices(self, n):
        # Vertices are 1-indexed
        self._vertices = [Vertex(i) for i in range(n + 1)]

    def _build_edges(self, edges):
        self._edges = []

        for edge in edges:
            if not edge:
                continue

            u, v, lb, c = map(int, edge.split())

            u = self._vertices[u]
            v = self._vertices[v]

            e = Edge(lb, c, u, v)
            u.outs.append(e)  # Forward edge
            v.ins.append(e)  # Backward edge
            self._edges.append(e)

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges


class Vertex:
    def __init__(self, key):
        self.key = key
        self.demand = 0
        self.outs = []
        self.ins = []

    def __repr__(self):
        return "Vertex(key={}, demand={}, outs={}, ins={})".format(
            self.key,
            self.demand,
            [e.to.key for e in self.outs],
            [e.fr.key for e in self.ins],
        )


class Edge:
    def __init__(self, lb, ub, fr, to):
        self.flow = 0
        self.lb, self.ub, self.fr, self.to = lb, ub, fr, to

    def __repr__(self):
        return "Edge(flow={}, lb={}, ub={}, fr={}, to={})".format(
            self.flow, self.lb, self.ub, self.fr.key, self.to.key
        )


def main():
    (nm, *edges) = sys.stdin.read().split("\n")
    n, m = map(int, nm.split())

    solver = FordFulkersonWithLowerBound(n, edges)

    if solver.solvable:
        print("YES")
        for edge in solver.edges:
            print(edge.flow)

    else:
        print("NO")


if __name__ == "__main__":
    main()
