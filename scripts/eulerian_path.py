def odd_vertices(n, edges):
    deg = [0] * n
    for (a,b,c) in edges:
        deg[a] += 1
        deg[b] += 1
    return [a for a in range(n) if deg[a] % 2]

def get_edge(edges, v1, v2):
    for (a,b,c) in edges:
        if (v1 == a and v2 == b) or (v1 == b and v2 == a):
            return (a,b,c)
    return None

def get_edges(edges, odd):
    res = []
    for v1 in odd:
        for v2 in odd:
            if v1 != v2:
                edge = get_edge(edges, v1, v2)
                if edge and not edge in res:
                    res.append(edge)
    return res

def get_shortest(edges):
    length = len(edges)
    if length == 0:
        return None
    shortest, index = edges[0][2], 0
    for i in range(1, length):
        (_,_,dist) = edges[i]
        if dist < shortest:
            shortest, index = dist, i
    return edges[index]

def to_eulerian(n, edges):
    odd = odd_vertices(n, edges)
    while len(odd) != 0 and len(odd) != 2:
        odd = odd_vertices(n, edges)
        edges2 = get_edges(edges, odd)
        a,b,c = get_shortest(edges2)
        edges.append((b,a,c))
        if a in odd:
            odd.remove(a)
        if b in odd:
            odd.remove(b)
        edges2.remove((a,b,c))
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
    edges = to_eulerian(n, edges)
    return find_eulerian_path(n, edges)
