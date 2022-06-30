from copy import copy

# return the list of odd vertices
def odd_vertices(n, edges):
    deg = [0] * n
    for (a,b,c) in edges:
        deg[a] += 1
        deg[b] += 1
    return [a for a in range(n) if deg[a] % 2]

# convert the graph to an adjacency list
def graph_to_adj(n, G):
    adj = [[] for _ in range(n)]
    for (a, b, w) in G:
        adj[a].append((b,w))
        adj[b].append((a,w))
    return adj

# application of dijkstra's algorithm to find the shortest path from a certain vertex to all other vertices
def dijkstra(G, s, path, n):
    adj = graph_to_adj(n, G)
    infi = 100000000
    dist = [infi for _ in range(len(adj))]
    visited = [False for _ in range(len(adj))]
    for i in range(len(adj)):       
        path[i] = -1
    dist[s] = 0
    path[s] = -1
    current = s
    sett = set()    
    while (True):
        visited[current] = True
        for i in range(len(adj[current])): 
            v,_ = adj[current][i];           
            if (visited[v]):
                continue
            sett.add(v)
            alt = dist[current] + adj[current][i][1]
            if (alt < dist[v]):      
                dist[v] = alt
                path[v] = current;       
        if current in sett:           
            sett.remove(current);       
        if (len(sett) == 0):
            break
        minDist = infi
        index = 0
        for a in sett:       
            if (dist[a] < minDist):          
                minDist = dist[a]
                index = a;          
        current = index
    return dist

# find the closest odd vertex to a certain vertex
def find_closest_odd(v, odd, dist):
    closest = odd[1]
    min_val = dist[closest]
    for v in odd[2:]:
        if dist[v] < min_val:
            closest = v
            min_val = dist[v]
    return closest, min_val

# convert the graph to an eulerian graph
def to_eulerian(n, edges):
    g = copy(edges)
    odd = odd_vertices(n, g)
    while len(odd) != 0 and len(odd) != 2:
        v = odd[0]
        path = [0 for _ in range(len(g))]
        dist = dijkstra(g, v, path, n)
        closest, w = find_closest_odd(v, odd, dist)
        g.append((v, closest, w))
        odd.remove(v)
        odd.remove(closest)
    return g

# find the edge with a certain vertex
def find_edge(edges, v):
    for (a,b,c) in edges:
        if a == v or b == v:
            return (a,b,c)
    return None

# find the eulerian path
def find_eulerian_path(n, edges):
    g = copy(edges)
    odd = odd_vertices(n, g)
    if len(odd) == 2:
        stack = [odd[0]]
    else:
        stack = [g[0][0]]
    path = []
    while stack:
        v = stack[-1]
        edge = find_edge(g, v)
        if edge:
            u = edge[0]
            if u == v:
                u = edge[1]
            stack.append(u)
            g.remove(edge)
        else:
            path.append(stack.pop())
    return path

# convert the given graph to an eulerian graph and find the eulerian path
def convert_and_find_eulerian_path(n, edges):
    G = to_eulerian(n, edges)
    return find_eulerian_path(n, G)
