# This script solves the Few problem using Dijkstra's algorithm with a weight function for the red vertices

import sys
import parse
from heapq import heapify, heappop, heappush

# Return Path of it exists, else return -1 (in Gex the answer is 0)
# find path from s to t
# weight for the reds, just do 0 for normal and 1 for red

# use heapq.heappush and heapq.heappop

def few(s, t, red, adj):
    distTo = {v: float('inf') for v in adj} #set all distances to INFINITY
    distTo[s] = 0 #distance at start vertex is 0

    pq = [(0, s)] #remember priority queue
    heapify(pq)

    while pq:
        for e in adj:
            

            





def main():
    s, t, vertices, red, adj, directed = parse.parse_file(sys.argv[1])
    result = few(s, t, red, adj)
    print(result)

if __name__ == "__main__":
    main()