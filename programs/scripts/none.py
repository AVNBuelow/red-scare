
from parse import parse, parse_file, parse_all

s, t, vertices, red, adj, directed = parse_file(sys.argv[1] if len(sys.argv) > 1 else "example1.txt")

P = set(vertices)

P -= red #this should remove all the vertices that are in the set red from the set P, and only black vertices should be left in P

start = {s}

changed = True
while changed:
    changed = False
    for u in list(R):
        for v in adj[u]:
            if v not in R:
                R.add(v)
                changed = True

print(R)



