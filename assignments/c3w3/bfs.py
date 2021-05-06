import sys
from collections import deque
from typing import List, NewType

Vertex = NewType("Vertex", int)
AdjacencyList = List[List[Vertex]]


def distance(adj: AdjacencyList, s: Vertex, t: Vertex):
    dist = [None] * len(adj)
    dist[s] = 0

    q = deque([s])

    while q:
        u = q.popleft()

        if u == t:
            return dist[u]

        for v in adj[u]:
            if dist[v] is None:
                q.append(v)
                dist[v] = dist[u] + 1

    return -1


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    s, t = data[2 * m] - 1, data[2 * m + 1] - 1
    print(distance(adj, s, t))
