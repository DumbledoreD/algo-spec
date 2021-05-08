import sys
from collections import deque
from typing import List, NewType

Vertex = NewType("Vertex", int)
AdjacencyList = List[List[Vertex]]
Cost = List[List[int]]


def shortest_paths(adj: AdjacencyList, cost: Cost, s: Vertex):
    dist = [float("inf")] * len(adj)
    dist[s] = 0

    iter_count = 0

    negative_cycle = deque()

    while True:
        relaxed = False
        iter_count += 1

        for i in range(len(adj)):
            u = (i + s) % len(adj)

            if dist[u] == float("inf"):
                continue

            for j, v in enumerate(adj[u]):
                dist_through_u = dist[u] + cost[u][j]
                if dist[v] > dist_through_u:
                    relaxed = True
                    dist[v] = dist_through_u

                    if iter_count == len(adj):
                        negative_cycle.append(v)

        if not relaxed or iter_count == len(adj):
            break

    while negative_cycle:
        u = negative_cycle.popleft()

        dist[u] = -float("inf")

        for v in adj[u]:
            if dist[v] != -float("inf"):
                negative_cycle.append(v)

    return dist


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
    s = data[0] - 1
    dist = shortest_paths(adj, cost, s)
    for d in dist:
        if d == float("inf"):
            print("*")
        elif d == -float("inf"):
            print("-")
        else:
            print(d)
