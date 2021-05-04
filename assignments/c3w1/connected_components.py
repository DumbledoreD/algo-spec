import sys


def number_of_components(adj):
    visited, cc_count = set(), 0

    for v in range(len(adj)):
        if v not in visited:
            stack = [v]

            while stack:
                cur_v = stack.pop()

                visited.add(cur_v)

                for next_v in adj[cur_v]:
                    if next_v not in visited:
                        stack.append(next_v)

            cc_count += 1

    return cc_count


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
    print(number_of_components(adj))
