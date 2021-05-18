import sys
from collections import deque


def build_adjacency_matrix(node_count, edges):
    matrix = [[0] * node_count for _ in range(node_count)]

    for u, v, c in edges:
        matrix[u][v] += c

    return matrix


def ford_fulkerson(adj_matrix, source, sink):
    flow = 0

    # For storing path discovered in bfs
    child_to_parent = [-1] * len(adj_matrix)

    while bfs(adj_matrix, source, sink, child_to_parent):

        path_flow = float("inf")

        # Calculate flow size
        v = sink
        while v != source:
            u = child_to_parent[v]

            path_flow = min(path_flow, adj_matrix[u][v])

            v = u

        flow += path_flow

        # Upadate network and residual network along the path, start from the sink
        v = sink
        while v != source:
            u = child_to_parent[v]

            adj_matrix[u][v] -= path_flow
            adj_matrix[v][u] += path_flow

            v = u

    return flow


def bfs(adj_matrix, source, sink, child_to_parent):
    visited = [False] * len(adj_matrix)

    queue = deque([source])

    while queue:
        u = queue.popleft()

        visited[u] = True

        for v in range(len(adj_matrix)):
            if not visited[v] and adj_matrix[u][v]:
                child_to_parent[v] = u

                if v == sink:
                    return True

                else:
                    queue.append(v)

    return False


if __name__ == "__main__":
    data = list(sys.stdin.read().split("\n"))

    node_count, edge_count = map(int, data[0].split())

    edges = []
    for edge in data[1:]:
        if edge:
            # Vertex key is 1-based
            u, v, c = list(map(int, edge.split()))
            edges.append((u - 1, v - 1, c))

    adj_matrix = build_adjacency_matrix(node_count, edges)

    max_flow = ford_fulkerson(adj_matrix, source=0, sink=node_count - 1)

    print(max_flow)
