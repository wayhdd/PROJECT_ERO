def odd_vertices(n, edges):
    deg = [0] * n
    for (a,b,c) in edges:
        deg[a] += 1
        deg[b] += 1
    return [a for a in range(n) if deg[a] % 2]

def graph_to_adj_weighted(G):
    m = 0
    for (a, b, w) in G:
        if (a > m):
            m = a
        if (b > m):
            m = b
    adj = [[] for _ in range(m + 1)]
    
    for (a, b, w) in G:
        adj[a].append((b,w))
    return adj

def dijkstra(G, s, path):
    adj = graph_to_adj_weighted(G)
    infi = 100000000
    dist = [infi for i in range(len(adj))]
    visited = [False for i in range(len(adj))]
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

def find_closest_odd(v, odd, dist):
    closest = odd[1]
    min_val = dist[closest]
    for v in odd[2:]:
        if dist[v] < min_val:
            closest = v
            min_val = dist[v]
    return closest, min_val

def to_eulerian(n, edges):
    odd = odd_vertices(n, edges)
    while len(odd) != 0 and len(odd) != 2:
        v = odd[0]
        path = [0 for i in range(len(edges))]
        dist = dijkstra(edges, v, path)
        closest, w = find_closest_odd(v, odd, dist)
        edges.append((v, closest, w))
        odd.remove(v)
        odd.remove(closest)
    return edges

def find_edge(edges, v):
    for (a,b,c) in edges:
        if a == v or b == v:
            return (a,b,c)
    return None

def find_eulerian_path(n, edges):
    odd = odd_vertices(n, edges)
    if len(odd) == 2:
        stack = [odd[0]]
    else:
        stack = [list(edges)[0]]
    path = []
    while stack:
        v = stack[-1]
        edge = find_edge(edges, v)
        if edge:
            u = edge[0]
            if u == v:
                u = edge[1]
            stack.append(u)
            edges.remove(edge)
        else:
            path.append(stack.pop())
    return path

def convert_and_find_eulerian_path(n, edges):
    G = to_eulerian(n, edges)
    return find_eulerian_path(len(G), G)
