from collections import deque
from parse import parse

def drop_same_colour_edges(adj, red):
    filtered = {}
    for u in adj:
        filtered[u] = []
        for v in adj[u]:
            if (u in red) != (v in red):
                filtered[u].append(v)
    return filtered


def has_alternating_path(adj, s, t):
    visited = {s}
    queue = deque([s])

    while queue:
        u = queue.popleft()
        if u == t:
            return True
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)

    return False


if __name__ == "__main__":
    s, t, vertices, red, adj, directed = parse()
    adj = drop_same_colour_edges(adj, red)
    if has_alternating_path(adj, s, t):
        print("true")
    else:
        print("false")