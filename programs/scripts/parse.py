# General parser to parse data as graphs for all problems

import sys
from pathlib import Path

# programs/data so it works from any working directory
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def parse(text=None):
    if text is None:
        text = sys.stdin.read()
    lines = [l for l in text.splitlines() if l.strip()]

    n, m, r = map(int, lines[0].split())
    s, t = lines[1].split()

    vertices = []
    red = set()
    for line in lines[2:2 + n]:
        parts = line.split()
        vertices.append(parts[0])
        if len(parts) > 1 and parts[1] == "*":
            red.add(parts[0])

    adj = {v: [] for v in vertices}
    directed = False
    for line in lines[2 + n:2 + n + m]:
        u, arrow, v = line.split()
        adj[u].append(v)
        if arrow == "--":
            adj[v].append(u)
        else:
            directed = True

    return s, t, vertices, red, adj, directed


def parse_file(name):
    path = Path(name)
    if not path.exists():
        path = DATA_DIR / name
    
    return parse(path.read_text())


def parse_all():
    for path in sorted(DATA_DIR.glob("*.txt")):
        yield path.name, parse(path.read_text())