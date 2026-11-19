import sys
import time
import threading
from collections import deque

from parse import parse, parse_file   # adjust to your parser's module name

TIME_LIMIT = 600  # seconds per search; the 1-hour cap is yours to enforce


## Code made in correspondence with AI - Claude.ai

class Timeout(Exception):
    pass


def bfs(src, g, allowed=None):
    """Vertices reachable from src in g (src included), restricted to `allowed` if given."""
    seen = {src}
    q = deque([src])
    while q:
        v = q.popleft()
        for w in g[v]:
            if w not in seen and (allowed is None or w in allowed):
                seen.add(w)
                q.append(w)
    return seen


def reverse(adj):
    radj = {v: [] for v in adj}
    for v in adj:
        for w in adj[v]:
            radj[w].append(v)
    return radj


def restrict(adj, keep):
    return {v: [w for w in adj[v] if w in keep] for v in keep}


# ---------- DAG: exact DP ----------
def dag_dp(adj, s, t, red):
    indeg = {v: 0 for v in adj}
    for v in adj:
        for w in adj[v]:
            indeg[w] += 1
    q = deque(v for v in adj if indeg[v] == 0)
    order = []
    while q:
        v = q.popleft()
        order.append(v)
        for w in adj[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                q.append(w)
    if len(order) != len(adj):
        return None  # has a cycle
    NEG = float("-inf")
    best = {v: NEG for v in adj}
    best[s] = red[s]
    for v in order:
        if best[v] == NEG:
            continue
        for w in adj[v]:
            best[w] = max(best[w], best[v] + red[w])
    return best[t]


# ---------- General: branch and bound ----------
def search(adj, s, t, red, deadline):
    """Max red vertices on a simple s-t path in adj. Returns (value, proven_optimal)."""
    radj = reverse(adj)
    visited = {s}
    best = -1
    nodes = 0

    def dfs(v, cur):
        nonlocal best, nodes
        if v == t:
            best = max(best, cur)
            return
        nodes += 1
        if nodes % 512 == 0 and time.time() > deadline:
            raise Timeout
        free = {x for x in adj if x not in visited}
        F = bfs(v, adj, free)
        if t not in F:
            return
        B = bfs(t, radj, free | {t})
        useful = (F & B) - {v}
        if cur + sum(red[x] for x in useful) <= best:
            return
        nbrs = [w for w in adj[v] if w in useful]
        nbrs.sort(key=lambda w: -red[w])  # try red neighbours first
        for w in nbrs:
            visited.add(w)
            dfs(w, cur + red[w])
            visited.discard(w)

    exact = True
    try:
        dfs(s, red[s])
    except Timeout:
        exact = False
    return best, exact


# ---------- Undirected: block-cut tree ----------
def biconnected_blocks(adj, s):
    disc = {s: 0}
    low = {s: 0}
    parent = {s: None}
    idx = {v: 0 for v in adj}
    timer = 1
    vstack = [s]
    call = [s]
    blocks = []
    while call:
        v = call[-1]
        if idx[v] < len(adj[v]):
            w = adj[v][idx[v]]
            idx[v] += 1
            if w not in disc:
                parent[w] = v
                disc[w] = low[w] = timer
                timer += 1
                vstack.append(w)
                call.append(w)
            elif w != parent[v]:
                low[v] = min(low[v], disc[w])
        else:
            call.pop()
            if call:
                p = call[-1]
                low[p] = min(low[p], low[v])
                if low[v] >= disc[p]:
                    comp = [p]
                    while True:
                        x = vstack.pop()
                        comp.append(x)
                        if x == v:
                            break
                    blocks.append(comp)
    return blocks


def solve_undirected(adj, s, t, red, deadline):
    blocks = biconnected_blocks(adj, s)
    # bipartite tree: vertex <-> block nodes
    tree = {}
    for i, comp in enumerate(blocks):
        b = ("B", i)
        tree[b] = list(comp)
        for v in comp:
            tree.setdefault(v, []).append(b)
    # path s -> t in tree
    prev = {s: None}
    q = deque([s])
    while q:
        x = q.popleft()
        if x == t:
            break
        for y in tree.get(x, []):
            if y not in prev:
                prev[y] = x
                q.append(y)
    chain = []
    x = t
    while x is not None:
        chain.append(x)
        x = prev[x]
    chain.reverse()  # s, B1, c1, B2, ..., t

    total = red[s]
    exact = True
    for i in range(1, len(chain), 2):
        a, blk, b = chain[i - 1], chain[i], chain[i + 1]
        members = set(blocks[blk[1]])
        sub = restrict(adj, members)
        val, ex = search(sub, a, b, red, deadline)
        exact &= ex
        total += val - red[a]  # a was already counted by the previous block
    return total, exact


# ---------- main solver ----------
def solve(s, t, vertices, red_set, adj, directed):
    red = {v: 1 if v in red_set else 0 for v in vertices}
    if s == t:
        return red[s], True
    fwd = bfs(s, adj)
    if t not in fwd:
        return -1, True
    keep = fwd & bfs(t, reverse(adj))
    adj = restrict(adj, keep)
    deadline = time.time() + TIME_LIMIT

    if directed:
        res = dag_dp(adj, s, t, red)
        if res is not None:
            return res, True
        return search(adj, s, t, red, deadline)
    return solve_undirected(adj, s, t, red, deadline)


def many(s, t, vertices, red_set, adj, directed):
    """Returns the max number of red vertices on a simple s,t-path, or -1 if no path exists."""
    result = []

    def run():
        result.append(solve(s, t, vertices, red_set, adj, directed)[0])

    sys.setrecursionlimit(1_000_000)
    threading.stack_size(256 * 1024 * 1024)
    th = threading.Thread(target=run)
    th.start()
    th.join()
    return result[0]


def main():
    data = parse_file(sys.argv[1]) if len(sys.argv) > 1 else parse()
    ans, exact = solve(*data)
    print(ans)
    if not exact:
        print("# timed out: value is only a lower bound", file=sys.stderr)


if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000)
    threading.stack_size(512 * 1024 * 1024)
    t = threading.Thread(target=main)
    t.start()
    t.join()