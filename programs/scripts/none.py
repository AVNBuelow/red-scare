import sys
from collections import deque
from parse import parse, parse_file

s, t, vertices, red, adj, directed = parse_file(sys.argv[1]) if len(sys.argv) > 1 else parse()

dist = {s: 0}
queue = deque([s])
answer = -1

while queue:
    u = queue.popleft()

    if u == t:
        answer = dist[u]
        break

    if u in red and u != s:
        continue

    for v in adj[u]:
        if v not in dist:
            dist[v] = dist[u] + 1
            queue.append(v)

print(answer)
