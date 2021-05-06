import heapq
import sys
from typing import List, NewType

Vertex = NewType("Vertex", int)
AdjacencyList = List[List[Vertex]]
Cost = List[List[int]]


def distance(adj: AdjacencyList, cost: AdjacencyList, s: Vertex, t: Vertex):
    dist = [float("inf")] * len(adj)
    prev = [None] * len(adj)
    dist[s] = 0

    dist_vertex_heap = [(d, v) for v, d in enumerate(dist)]
    heapq.heapify(dist_vertex_heap)

    while dist_vertex_heap:
        d, u = heapq.heappop(dist_vertex_heap)

        # Using `insert` instead of `change_priority` for better runtime.
        # Hence ignore items with d that are stale.
        if d != dist[u]:
            continue

        if u == t:
            return -1 if d == float("inf") else d

        for i, v in enumerate(adj[u]):
            dist_through_u = dist[u] + cost[u][i]
            if dist[v] > dist_through_u:
                dist[v] = dist_through_u
                prev[v] = u
                heapq.heappush(dist_vertex_heap, (dist[v], v))

    return -1


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(
        zip(zip(data[0 : (3 * m) : 3], data[1 : (3 * m) : 3]), data[2 : (3 * m) : 3])
    )
    data = data[3 * m :]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for ((a, b), w) in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)
    s, t = data[0] - 1, data[1] - 1
    print(distance(adj, cost, s, t))
