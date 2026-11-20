import sys
from collections import deque
from parse import parse_file

s, t, vertices, red, adj, directed = parse_file(sys.argv[1] if len(sys.argv) > 1 else "example1.txt")

P = set(vertices)

P -= red #this should remove all the vertices that are in the set red from the set P, and only black vertices should be left in P

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
