import sys
from collections import deque
from typing import List, NewType

Vertex = NewType("Vertex", int)
AdjacencyList = List[List[Vertex]]


def bipartite(adj: AdjacencyList) -> bool:
    colors = [None] * len(adj)

    for vertex in range(len(adj)):
        if colors[vertex] is None:

            colors[vertex] = 0
            q = deque([vertex])

            while q:
                u = q.popleft()

                for v in adj[u]:
                    if colors[v] is not None:
                        if colors[v] == colors[u]:
                            return False
                    else:
                        q.append(v)
                        colors[v] = (colors[u] + 1) % 2

    return True


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
    print(int(bipartite(adj)))
