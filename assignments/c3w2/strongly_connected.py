import sys
from collections import deque
from typing import Deque, List, NewType, Set

sys.setrecursionlimit(10 ** 6)

Vertex = NewType("Vertex", int)
AdjacencyList = List[List[Vertex]]


def number_of_strongly_connected_components(adj: AdjacencyList) -> int:
    scc_count = 0

    reverse_graph = get_reverse_graph(adj)

    ordered_vertices = sort_by_post_orders(reverse_graph)

    visited = set()

    for v in ordered_vertices:
        if v not in visited:
            stack = [v]

            while stack:
                cur_node = stack.pop()
                visited.add(cur_node)

                for next_v in adj[cur_node]:
                    if next_v not in visited:
                        stack.append(next_v)

            scc_count += 1

    return scc_count


def get_reverse_graph(adj: AdjacencyList) -> AdjacencyList:
    reverse_adj = [[] for _ in range(len(adj))]

    for u, vs in enumerate(adj):
        for v in vs:
            reverse_adj[v].append(u)

    return reverse_adj


def sort_by_post_orders(adj: AdjacencyList) -> Deque[Vertex]:
    visited = set()
    order = deque()

    for v in range(len(adj)):
        if v not in visited:
            dfs(v, adj, visited, order)

    return order


def dfs(v: Vertex, adj: AdjacencyList, visited: Set[Vertex], order: Deque[Vertex]):
    visited.add(v)

    for next_v in adj[v]:
        if next_v not in (visited):
            dfs(next_v, adj, visited, order)

    order.appendleft(v)


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(number_of_strongly_connected_components(adj))
