from collections import defaultdict, deque
from parse import parse_file, parse_all

# Check
def solve_some(graph, s, t, red, directed):
    if t not in reachable_from(graph, s):
        return False

    if s in red or t in red:
        return True

    if directed:
        if has_cycle(graph):
            return "?!"
        return some_dag(graph, s, t, red)
    return some_undirected(graph, s, t, red)

# Searching a graph with BFS
def reachable_from(graph, start):
    found = {start}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in found:
                found.add(v)
                queue.append(v)
    return found

def reverse_graph(graph):
    rev = {v: [] for v in graph}
    for u in graph:
        for v in graph[u]:
            rev[v].append(u)
    return rev

def has_cycle(graph):
    indegree = {v: 0 for v in graph}
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1

    queue = deque(v for v in graph if indegree[v] == 0)
    removed = 0
    while queue:
        u = queue.popleft()
        removed += 1
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    return removed != len(graph)

# First case : DAGs

def some_dag(graph, s, t, red):
    from_s = reachable_from(graph, s)
    to_t = reachable_from(reverse_graph(graph), t)
    return any(r in from_s and r in to_t for r in red)

# Second case : Undirected

def some_undirected(graph, s, t, red):
    from_s = reachable_from(graph, s)
    for r in red:
        if r in from_s and two_disjoint_paths(graph, r, s, t):
            return True
    return False

class FlowNetwork:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v, cap):
        self.graph[u].append([v, cap, len(self.graph[v])])
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])

    def augment(self, source, sink):
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for i, (v, cap, _) in enumerate(self.graph[u]):
                if cap > 0 and v not in parent:
                    parent[v] = (u, i)
                    queue.append(v)

        if sink not in parent:
            return False

        v = sink
        while parent[v] is not None:
            u, i = parent[v]
            edge = self.graph[u][i]
            edge[1] -= 1
            self.graph[v][edge[2]][1] += 1
            v = u
        return True

def two_disjoint_paths(graph, r, s, t):
    net = FlowNetwork()
    for v in graph:
        net.add_edge(("in", v), ("out", v), 1)
        for w in graph[v]:
            net.add_edge(("out", v), ("in", w), 1)
    net.add_edge(("out", s), "SINK", 1)
    net.add_edge(("out", t), "SINK", 1)

    source = ("out", r)
    flow = 0
    for _ in range(2):
        if not net.augment(source, "SINK"):
            break
        flow += 1
    return flow == 2