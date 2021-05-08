import sys
from collections import deque
from typing import Deque, List, NewType

Vertex = NewType("Vertex", int)
AdjacencyList = List[List[Vertex]]


def dfs(v: Vertex, adj: AdjacencyList, visited: List[Vertex], order: Deque[Vertex]):
    visited[v] = 1

    for next_v in adj[v]:
        if not visited[next_v]:
            dfs(next_v, adj, visited, order)

    order.appendleft(v)


def top_sort(adj: AdjacencyList) -> Deque[Vertex]:
    visited = [0] * len(adj)
    order = deque()

    for v in range(len(adj)):
        if not visited[v]:
            dfs(v, adj, visited, order)

    return order


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    order = top_sort(adj)
    for x in order:
        print(x + 1, end=" ")
