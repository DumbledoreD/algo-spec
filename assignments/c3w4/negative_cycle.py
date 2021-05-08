import sys
from typing import List, NewType

Vertex = NewType("Vertex", int)
AdjacencyList = List[List[Vertex]]
Cost = List[List[int]]


def negative_cycle(adj: AdjacencyList, cost: Cost) -> bool:
    dist = [float("inf")] * len(adj)
    prev = [None] * len(adj)

    iter_count = 0

    while True:
        relaxed = False

        for u in range(len(adj)):
            # Note this, a neat way to handle disjoint sets if the "correct" distance
            # is not required
            if dist[u] == float("inf"):
                dist[u] = 0

            for i, v in enumerate(adj[u]):
                dist_through_u = dist[u] + cost[u][i]
                if dist[v] > dist_through_u:
                    relaxed = True
                    dist[v] = dist_through_u
                    prev[v] = u

        iter_count += 1

        if not relaxed or iter_count == len(adj):
            break

    return iter_count == len(adj) and relaxed


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
    print(int(negative_cycle(adj, cost)))
