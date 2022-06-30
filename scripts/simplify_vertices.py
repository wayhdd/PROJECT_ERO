# extract all vertices from a list of edges
def extract_vertices(edges):
    vertices = []
    for (a,b,_) in edges:
        if a not in vertices:
            vertices.append(a)
        if b not in vertices:
            vertices.append(b)
    return vertices

# replace vertices with indices
def replace_vertices(edges, l):
    for i in range(len(edges)):
        (a,b,c) = edges[i]
        edges[i] = (l.index(a), l.index(b), c)
    return edges

# replace indices with vertices
def replace_vertices_back(edges, l):
    for i in range(len(edges)):
        (a,b,c) = edges[i]
        edges[i] = (l[a], l[b], c)
    return edges

# replace indices with vertices in a path
def replace_vertices_back_in_path(path, l):
    for i in range(len(path)):
        path[i] = l[path[i]]
    return path
