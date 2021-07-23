import sys
from collections import deque
from enum import Enum


class FlowDirection(Enum):
    Forward = 0
    Backward = 1


class EdmondsKarpWithLowerBound:
    def __init__(self, n, edges):
        graph = GraphBuilder(n, edges)
        self._vertices, self._edges = graph.vertices, graph.edges

        self._remove_lower_bound()
        self._remove_demand()
        self._do_edmonds_karp()
        self._restore_lower_bound()

    def _remove_lower_bound(self):
        for edge in self._edges:
            edge.capacity -= edge.lb
            edge.fr.demand += edge.lb
            edge.to.demand -= edge.lb

    def _remove_demand(self):
        self._super_source = Vertex("source")
        self._super_sink = Vertex("sink")

        for vertex in self._vertices:
            if vertex.demand < 0:
                self._super_source.outs.append(
                    Edge(0, -vertex.demand, self._super_source, vertex)
                )

            elif vertex.demand > 0:
                vertex.outs.append(Edge(0, vertex.demand, vertex, self._super_sink))

    def _do_edmonds_karp(self):
        while True:
            path = self._bfs()

            if not path:
                break

            # Find the min flow in the path
            path_flow = float("inf")

            for direction, edge in path:
                if direction == FlowDirection.Forward:
                    path_flow = min(path_flow, edge.capacity - edge.flow)

                elif direction == FlowDirection.Backward:
                    path_flow = min(path_flow, edge.flow)

            # Update the flow along the path
            for direction, edge in path:
                if direction == FlowDirection.Forward:
                    edge.flow += path_flow

                elif direction == FlowDirection.Backward:
                    edge.flow -= path_flow

    def _bfs(self):
        seen = set()
        seen.add(self._super_source)

        queue = deque([(self._super_source, [])])

        while queue:
            u, path = queue.popleft()

            for edge in u.outs:
                direction = (
                    FlowDirection.Forward if edge.fr == u else FlowDirection.Backward
                )

                if (
                    (edge.to in seen)
                    or (
                        direction == FlowDirection.Forward
                        and edge.flow == edge.capacity
                    )
                    or (direction == FlowDirection.Backward and edge.flow == 0)
                ):
                    continue

                new_path = path + [(direction, edge)]

                if edge.to == self._super_sink:
                    return new_path

                else:
                    queue.append((edge.to, new_path))
                    seen.add(edge.to)

    def _restore_lower_bound(self):
        for edge in self._edges:
            edge.flow += edge.lb

            edge.fr.demand -= edge.lb
            edge.to.demand += edge.lb

            edge.fr.net_flow -= edge.flow
            edge.to.net_flow += edge.flow

    @property
    def solvable(self):
        for v in self._vertices:
            if v.net_flow != 0:
                return False
        return True

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
            u.outs.append(e)
            v.outs.append(e)  # Add to v.outs as backward edge
            self._edges.append(e)

            # dv' = dv - (Lin - Lout)
            # dv - original vertex demand
            # Lin - sum of vertex input edges lower bounds
            # Lout - sum of vertex output edges lower bounds
            u.demand += lb
            v.demand -= lb

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges


class Vertex:
    def __init__(self, key):
        self.key = key
        self.net_flow = 0
        self.demand = 0
        self.outs = []

    def __repr__(self):
        return "Vertex(key={}, net_flow={}, demand={}, outs={})".format(
            self.key, self.net_flow, self.demand, [e.to.key for e in self.outs]
        )


class Edge:
    def __init__(self, lb, capacity, fr, to):
        self.flow = 0
        self.lb, self.capacity, self.fr, self.to = lb, capacity, fr, to

    def __repr__(self):
        return "Edge(flow={}, lb={}, capacity={}, fr={}, to={})".format(
            self.flow, self.lb, self.capacity, self.fr.key, self.to.key
        )


def main():
    (
        nm,
        *edges,
    ) = """\
3 3
1 2 1 3
2 3 2 4
3 1 1 2
""".split(
        "\n"
    )
    n, m = map(int, nm.split())

    solver = EdmondsKarpWithLowerBound(n, edges)

    if solver.solvable:
        print("YES")
        for edge in solver.edges:
            print(edge.flow)

    else:
        print("NO")


if __name__ == "__main__":
    main()
