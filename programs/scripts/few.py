# This script solves the Few problem using Dijkstra's algorithm with a weight function for the red vertices

import sys
import parse
from collections import deque
from heapq import heapify, heappop, heappush

# Dijkstra's algorithm with a weight function for the red vertices
def Dijkstra(s, t, red, adj):
    distTo = {v: float('inf') for v in adj} #set all distances to INFINITY
    distTo[s] = 1 if s in red else 0

    pq = [(distTo[s], s)] #remember priority queue
    heapify(pq)

    while pq:
        d, u = heappop(pq)

        if u == t:
            return d

        for v in adj[u]:
            weight = 1 if v in red else 0

            if d + weight < distTo[v]:
                distTo[v] = d + weight
                heappush(pq, (distTo[v], v))

    return -1

# 0-1 BFS algorithm with a weight function for the red vertices - used
def BFS(s, t, red, adj):
    distTo = {v: sys.maxsize for v in adj} # set all distances to MAX
    distTo[s] = 1 if s in red else 0 

    dq = deque()
    dq.append(s)

    while dq:
        u = dq.popleft()

        if u == t:
            return distTo[u]
        
        for v in adj[u]:
            weight = 1 if v in red else 0 

            if distTo[u] + weight < distTo[v]:
                distTo[v] = distTo[u] + weight

                if weight == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    
    return distTo[t] if distTo[t] != sys.maxsize else -1

def main():
    for name, (s, t, vertices, red, adj, directed) in parse.parse_all():
        result = BFS(s, t, red, adj)
        return result
        
    
if __name__ == "__main__":
    main()
