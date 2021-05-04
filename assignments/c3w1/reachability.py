import sys


def reach(adj, x, y):
    stack = [x]
    visited = set()

    while stack:
        cur_v = stack.pop()

        if cur_v == y:
            return True

        visited.add(cur_v)

        for v in adj[cur_v]:
            if v not in visited:
                stack.append(v)

    return False


if __name__ == "__main__":
    data = list(map(int, sys.stdin.read().split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    x, y = data[2 * m :]
    adj = [[] for _ in range(n)]
    x, y = x - 1, y - 1
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    print(int(reach(adj, x, y)))
