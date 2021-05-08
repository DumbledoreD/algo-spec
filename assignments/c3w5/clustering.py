import math
import sys
from itertools import combinations
from operator import attrgetter
from typing import List, NewType

VertexId = NewType("VertexId", int)


# Not compatible with grader

# @dataclass
# class Vertex:
#     i: VertexId
#     x: int
#     y: int


# @dataclass
# class Edge:
#     u: Vertex
#     v: Vertex

#     @property
#     def weight(self) -> float:
#         return math.sqrt((self.u.x - self.v.x) ** 2 + (self.u.y - self.v.y) ** 2)


class Vertex:
    def __init__(self, i: VertexId, x: int, y: int):
        self.i, self.x, self.y = i, x, y


class Edge:
    def __init__(self, u: Vertex, v: Vertex):
        self.u, self.v = u, v

    @property
    def weight(self) -> float:
        return math.sqrt((self.u.x - self.v.x) ** 2 + (self.u.y - self.v.y) ** 2)


class DisjointSet:
    def __init__(self, vertices: List[Vertex]):
        self.child_to_parent = list(range(len(vertices)))
        self.rank = [0] * len(vertices)

    def find(self, i: VertexId) -> VertexId:
        parent = self.child_to_parent[i]

        if parent == i:
            return i

        true_parent = self.find(parent)

        self.child_to_parent[i] = true_parent

        return true_parent

    def union(self, u: VertexId, v: VertexId):
        u_parent = self.find(u)
        v_parent = self.find(v)

        if u_parent == v_parent:
            return

        u_parent_rank, v_parent_rank = self.rank[u_parent], self.rank[v_parent]

        if u_parent_rank < v_parent_rank:
            self.child_to_parent[u_parent] = v_parent
        else:
            self.child_to_parent[v_parent] = u_parent

            if u_parent_rank == v_parent_rank:
                self.rank[u_parent] += 1


def build_graph(x: List[int], y: List[int]) -> (List[Vertex], List[Edge]):
    vertices = [Vertex(i, x, y) for i, (x, y) in enumerate(zip(x, y))]
    edges = [Edge(u, v) for u, v in combinations(vertices, 2)]
    return vertices, edges


def clustering(x: List[int], y: List[int], k: int) -> float:
    vertices, edges = build_graph(x, y)
    ds = DisjointSet(vertices)

    edges.sort(key=attrgetter("weight"))

    group_count = len(vertices)

    for edge in edges:
        if ds.find(edge.u.i) != ds.find(edge.v.i):
            if group_count == k:
                return edge.weight

            ds.union(edge.u.i, edge.v.i)
            group_count -= 1

    return -1


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    data = data[1:]
    x = data[0 : 2 * n : 2]
    y = data[1 : 2 * n : 2]
    data = data[2 * n :]
    k = data[0]
    print("{0:.9f}".format(clustering(x, y, k)))
