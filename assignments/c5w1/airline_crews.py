import sys
from collections import deque


def find_bipartite_matching(u_count, v_count, edges):
    adj_matrix = build_adjacency_matrix(u_count, v_count, edges)

    adj_matrix = ford_fulkerson_bipartitie(
        adj_matrix, source=0, sink=u_count + v_count + 1
    )

    matches = get_matches_from_adj_matrix(adj_matrix, u_count, v_count)

    return matches


def build_adjacency_matrix(u_count, v_count, edges):
    # +2 for source and sink
    node_count = u_count + v_count + 2
    matrix = [[0] * node_count for _ in range(node_count)]

    u_offset = 1
    v_offset = 1 + u_count

    for u, vs in enumerate(edges):
        for v, val in enumerate(vs):
            matrix[u + u_offset][v + v_offset] = val

    # Connect source to u
    for u in range(u_count):
        matrix[0][u + u_offset] = 1

    # Connect v to sink
    for v in range(v_count):
        matrix[v + v_offset][-1] = 1

    return matrix


def ford_fulkerson_bipartitie(adj_matrix, source, sink):
    # For storing path discovered in bfs
    child_to_parent = [-1] * len(adj_matrix)

    while bfs(adj_matrix, source, sink, child_to_parent):
        # Upadate network and residual network along the path, start from the sink
        v = sink
        while v != source:
            u = child_to_parent[v]

            adj_matrix[u][v] -= 1
            adj_matrix[v][u] += 1

            v = u

    return adj_matrix


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


def get_matches_from_adj_matrix(adj_matrix, u_count, v_count):
    u_to_v = [-1] * u_count

    u_index_offset = 1
    v_index_offset = 1 + u_count
    # Note, look at the resisual graph to tell if there's a match
    for u in range(u_count):
        for v in range(v_count):
            if adj_matrix[v + v_index_offset][u + u_index_offset] == 1:
                u_to_v[u] = v
                break

    return u_to_v


if __name__ == "__main__":
    data = sys.stdin.read().split("\n")

    flight_count, crew_count = map(int, data[0].split())

    edges = []
    for edge in data[1:]:
        if edge:
            edges.append(list(map(int, edge.split())))

    matches = find_bipartite_matching(flight_count, crew_count, edges)

    print(" ".join([str(crew if crew == -1 else crew + 1) for crew in matches]))
