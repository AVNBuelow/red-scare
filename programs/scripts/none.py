import sys
from collections import deque
from parse import parse, parse_file


def none(s, t, red, adj):
    """Length of a shortest s,t-path whose internal vertices are not red, or -1."""
    dist = {s: 0}
    queue = deque([s])

    while queue:
        u = queue.popleft()

        if u == t:
            return dist[u]

        if u in red and u != s:
            continue

        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)

    return -1


def main():
    s, t, red, adj = parse_file(sys.argv[1]) if len(sys.argv) > 1 else parse()
    print(none(s, t, red, adj))


if __name__ == "__main__":
    main()
