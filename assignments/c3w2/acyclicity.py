import sys
from typing import List, NewType, Set

Vertex = NewType("Vertex", int)
AdjacencyList = List[List[Vertex]]


def acyclic(adj: AdjacencyList) -> bool:
    visited = set()

    for v in range(len(adj)):
        if v not in visited:
            try:
                detect_cycle_dfs(v, adj, visited, set())
            except Exception:
                return True

    return False


def detect_cycle_dfs(
    v: Vertex, adj: AdjacencyList, visited: Set(Vertex), recursion_stack: Set(Vertex)
) -> bool:
    visited.add(v)

    recursion_stack.add(v)

    for next_v in adj[v]:
        if next_v in recursion_stack:
            raise Exception("cycle")

        if next_v not in visited:
            detect_cycle_dfs(next_v, adj, visited, recursion_stack)

    recursion_stack.remove(v)


if __name__ == "__main__":
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(int(acyclic(adj)))
