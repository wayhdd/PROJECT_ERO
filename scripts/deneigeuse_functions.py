from copy import copy
import sys
sys.path.append('./scripts')
import simplify_vertices as sv

def dijkstra(G, start, end, is_directed):
    '''
    Function to find the shortest path in a graph G from vertex start
    to vertex end. is_directed is bool to consider graph directed or not
    Function returns a tuple ([path] , path_distance)
    '''
    # conversions
    graph = {}
    # calculate total number of vertices
    total = 0
    for (a, b, w) in G:
        if a > total:
            total = a
        if b > total:
            total = b
    for i in range(total + 1):
        graph[i] = {}
    for (a, b, w) in G:
        graph[a][b] = w
        if not is_directed: # if the graph is not directed add the same edge but in reverse direction
            graph[b][a] = w
    
    # empty dictionary to hold distances
    distances = {} 
    # list of vertices in path to current vertex
    predecessors = {} 
    
    # get all the vertices that need to be assessed
    to_assess = graph.keys() 

    # set all initial distances to infinity
    #  and no predecessor for any node
    for node in graph:
        distances[node] = float('inf')
        predecessors[node] = None
    
    # set the initial collection of 
    # permanently labelled nodes to be empty
    sp_set = []

    # set the distance from the start vertex to be 0
    distances[start] = 0
    
    # as long as there are still vertices to assess:
    while len(sp_set) < len(to_assess):

        # chop out any vertices with a permanent label
        still_in = {node: distances[node]\
                    for node in [node for node in\
                    to_assess if node not in sp_set]}

        # find the closest node to the current vertex
        closest = min(still_in, key = distances.get)

        # and add it to the permanently labelled vertices
        sp_set.append(closest)
        
        # then for all the neighbours of 
        # the closest vertex (that was just added to
        # the permanent set)
        for node in graph[closest]:
            # if a shorter path to that node can be found
            if distances[node] > distances[closest] +\
                       graph[closest][node]:

                # update the distance with 
                # that shorter distance
                distances[node] = distances[closest] +\
                       graph[closest][node]

                # set the predecessor for that node
                predecessors[node] = closest
                
    # once the loop is complete the final 
    # path needs to be calculated - this can
    # be done by backtracking through the predecessors
    path = [end]
    while start not in path:
        if (predecessors[path[-1]] == None): # it means that path doesnt exist
            return None, 0
        path.append(predecessors[path[-1]])
    
    # return the path in order start -> end, and it's cost
    return path[::-1], distances[end]

def directed_to_eulerian(G):
    '''
    This functions converts directed graph G to a directed semi-eulerian
    graph without modifying G. 
    The returned graph will surely have an eulerian directed path.
    '''
    # create a copy of G to not modify the initial graph
    G_copy = copy(G)
    # create lists of vertices with their in and out degrees (vertice_number, inv, outv)
    in_bigger = [] # in = out + 1
    out_bigger = [] # out = in + 1
    in_dominant = [] # in > out + 1
    out_dominant = [] # out > in + 1
    m = 0
    for (a, b, w) in G:
        if (a > m):
            m = a
        if (b > m):
            m = b
    for i in range(m + 1): # for each vertice of the graph count the number of in and out
        inv = 0
        outv = 0
        for (a, b, w) in G:
            if (i == a):
                outv += 1
            if (i == b):
                inv += 1
        # adding all vertices in their respective list        
        if (inv == outv + 1):
            in_bigger.append((i, inv, outv))
        elif (outv == inv + 1):
            out_bigger.append((i, inv, outv))
        elif (inv > outv + 1):
            in_dominant.append((i, inv, outv))
        elif (inv != outv):
            out_dominant.append((i, inv, outv))
    
    while (len(out_bigger) > 1 or len(in_bigger) > 1) or len(in_dominant) > 0 or len(out_dominant) > 0:
        while (len(in_bigger) > 1):
            (i, inv, outv) = in_bigger[0]
            if (len(out_dominant) > 0):
                (i2, inv2, outv2) = out_dominant[0]
                # find the shortest distance using dijkstra to create new edge
                path, dist = dijkstra(G, i, i2, is_directed=False)
                # adding edge 1 -> 2
                G_copy.append((i, i2, dist))
                # removing first vertice from the list because it now has equla number of in and out
                in_bigger.pop(0)
                if (inv2 + 1 == outv2):
                    out_dominant.pop(0) # if new inv == outv remove
                elif (inv2 + 2 == outv2):
                    out_dominant.pop(0)
                    out_bigger.append(((i2, inv2 + 1, outv2))) # if 'out dominant' node becames 'out bigger' node
                else:
                    out_dominant[0] = (i2, inv2 + 1, outv2) # if its not equal just update new inv
            elif (len(out_bigger) > 0):
                (i2, inv2, outv2) = out_bigger[0]
                # adding edge 1 -> 2
                # find the shortest distance using dijkstra to create new edge
                path, dist = dijkstra(G, i, i2, is_directed=False)
                G_copy.append((i, i2, dist))
                in_bigger.pop(0)
                out_bigger.pop(0)
            else:
                print("1 The graph is not connected ! Try to redo the algorithm on a piece of paper !")
                return G_copy
            
        while (len(out_bigger) > 1):
            (i, inv, outv) = out_bigger[0]
            if (len(in_dominant) > 0):
                (i2, inv2, outv2) = in_dominant[0]
                # find the shortest distance using dijkstra to create new edge
                path, dist = dijkstra(G, i2, i, is_directed=False)
                G_copy.append((i2, i, dist))
                out_bigger.pop(0)
                if (outv2 + 1 == inv2):
                    in_dominant.pop(0)
                elif (outv2 + 2 == inv2):
                    in_dominant.pop(0)
                    in_bigger.append(((i2, inv2, outv2 + 1))) # if 'in dominant' node becames 'in bigger' node
                else:
                    in_dominant[0] = (i2, inv2, outv2 + 1)
            elif (len(in_bigger) > 0):
                (i2, inv2, outv2) = in_bigger[0]
                # find the shortest distance using dijkstra to create new edge
                path, dist = dijkstra(G, i2, i, is_directed=False)
                G_copy.append((i2, i, dist))
                out_bigger.pop(0)
                in_bigger.pop(0)
            else:
                print("2 The graph is not connected ! Try to redo the algorithm on a piece of paper !")
                return G_copy
            
        while (len(in_dominant) > 0):
            (i, inv, outv) = in_dominant[0]
            if (len(out_dominant) > 0):
                (i2, inv2, outv2) = out_dominant[0]
                # find the shortest distance using dijkstra to create new edge
                path, dist = dijkstra(G, i, i2, is_directed=False)
                G_copy.append((i, i2, dist))
                if (outv + 1 == inv):
                    in_dominant.pop(0)
                elif (outv + 2 == inv):
                    in_dominant.pop(0)
                    in_bigger.append((i, inv, outv + 1)) # if 'in dominant' node becames 'in bigger' node
                else:
                    in_dominant[0] = (i, inv, outv + 1)
                # do the same for out_dominant
                if (inv2 + 1 == outv2):
                    out_dominant.pop(0)
                elif (inv2 + 2 == outv2):
                    out_dominant.pop(0)
                    out_bigger.append((i2, inv2 + 1, outv2)) # if 'in dominant' node becames 'in bigger' node
                else:
                    out_dominant[0] = (i2, inv2 + 1, outv2)
            elif (len(out_bigger) > 0):
                (i2, inv2, outv2) = out_bigger[0]
                # find the shortest distance using dijkstra to create new edge
                path, dist = dijkstra(G, i, i2, is_directed=False)
                G_copy.append((i, i2, dist))
                out_bigger.pop(0)
                if (outv + 1 == inv):
                    in_dominant.pop(0)
                elif (outv + 2 == inv):
                    in_dominant.pop(0)
                    in_bigger.append((i, inv, outv + 1)) # if 'in dominant' node becames 'in bigger' node
                else:
                    in_dominant[0] = (i, inv, outv + 1)
            
            else:
                print("3 The graph is not connected ! Try to redo the algorithm on a piece of paper !")
                return G_copy
            
        while (len(out_dominant) > 0):
            (i, inv, outv) = out_dominant[0]
            if (len(in_dominant) > 0):
                (i2, inv2, outv2) = in_dominant[0]
                # find the shortest distance using dijkstra to create new edge
                path, dist = dijkstra(G, i, i2, is_directed=False)
                G_copy.append((i, i2, dist))
                if (inv + 1 == outv):
                    out_dominant.pop(0)
                elif (inv + 2 == outv):
                    out_dominant.pop(0)
                    out_bigger.append((i, inv + 1, outv)) # if 'in dominant' node becames 'in bigger' node
                else:
                    out_dominant[0] = (i, inv + 1, outv)
                # do the same for in_dominant
                if (outv2 + 1 == inv2):
                    in_dominant.pop(0)
                elif (outv2 + 2 == inv2):
                    in_dominant.pop(0)
                    in_bigger.append((i2, inv2, outv2 + 1)) # if 'in dominant' node becames 'in bigger' node
                else:
                    in_dominant[0] = (i2, inv2, outv2 + 1)
            elif (len(in_bigger) > 0):
                (i2, inv2, outv2) = in_bigger[0]
                # find the shortest distance using dijkstra to create new edge
                path, dist = dijkstra(G, i2, i, is_directed=False)
                G_copy.append((i2, i, dist))
                in_bigger.pop(0)
                if (inv + 1 == outv):
                    out_dominant.pop(0)
                elif (inv + 2 == outv):
                    out_dominant.pop(0)
                    out_bigger.append((i, inv + 1, outv)) # if 'in dominant' node becames 'in bigger' node
                else:
                    out_dominant[0] = (i, inv + 1, outv)
            
            else:
                print("4 The graph is not connected ! Try to redo the algorithm on a piece of paper !")
                return G_copy
    
    return G_copy


def graph_to_adj(G):
    '''
    Sub function converting our graph to an adj list,
    used in get_eulerian_path function
    '''
    m = 0
    for (a, b, w) in G:
        if (a > m):
            m = a
        if (b > m):
            m = b
    adj = [[] for _ in range(m + 1)]
    
    for (a, b, w) in G:
        adj[a].append(b)
    return adj
    
def get_eulerian_path(G):
    '''
    Hierholzer’s Algorithm for directed graph.
    This functions returns eulerian path from the graph G,
    as a list of vertices.
    '''
    adj = graph_to_adj(G)
    # adj represents the adjacency list of
    # the directed graph
    # edge_count represents the number of edges
    # emerging from a vertex
        
    edge_count = dict()
  
    for i in range(len(adj)):
  
        # find the count of edges to keep track
        # of unused edges
        edge_count[i] = len(adj[i])
  
    if len(adj) == 0:
        return # empty graph
  
    # Maintain a stack to keep vertices
    curr_path = []
  
    # vector to store final circuit
    circuit = []
  
    # find the start vertex (indeg + 1 = outdeg)
    # create lists of vertices with their in and out (vertice_number, inv, outv)
    start_vertex = (0, 0, 0) # out = in + 1
    m = 0
    for (a, b, w) in G:
        if (a > m):
            m = a
        if (b > m):
            m = b
    for i in range(m + 1): # for each vertice of the graph count the number of in and out
        inv = 0
        outv = 0
        for (a, b, w) in G:
            if (i == a):
                outv += 1
            if (i == b):
                inv += 1
        # adding all vertices in their respective list 
        if (outv == inv + 1):
            start_vertex = (i, inv, outv)
    
    # find the end vertex (outdeg + 1 = indeg) if there is no end vertex
    
    
    # start from the start_vertex, if there is no start vertex, start from 0
    curr_path.append(start_vertex[0])
    curr_v = start_vertex[0] # Current vertex
  
    while len(curr_path): # while stack isn't empty
  
        # If there's remaining edge
        if edge_count[curr_v]: # while in edge_count list there is still some edges 
  
            # Push the vertex
            curr_path.append(curr_v)
  
            # Find the next vertex using an edge
            next_v = adj[curr_v][-1]
  
            # and remove that edge
            edge_count[curr_v] -= 1
            adj[curr_v].pop()
  
            # Move to next vertex
            curr_v = next_v
  
        # back-track to find remaining path
        else:
            circuit.append(curr_v)
  
            # Back-tracking
            curr_v = curr_path[-1]
            curr_path.pop()
  
    # we've got the path, now return its reverse
    rev = []
    for item in circuit[::-1]:
        rev.append(item)
    return rev


def is_in_graph(G, x, y):
    '''
    Sub function used in replace_nodes.
    '''
    for (a, b, w) in G:
        if (x == a and y == b):
            return True
    return False

def replace_nodes(G, path):
    '''
    Function modifying the elerian path 'path' by considering the 
    initial graph G.
    This function returns a new path as a list, the new returned path
    exists in the real initial graph G.
    '''
    i = 0
    while i < len(path) - 1:
        a = path[i]
        b = path[i + 1]
        if (not is_in_graph(G, a, b)):
            p, d = dijkstra(G, a, b, is_directed=True)
            if (d == 0):
                p, d = dijkstra(G, a, b, is_directed=False)
            path.pop(i)
            path.pop(i)
            for e in p:
                path.insert(i, e)
                i += 1
            if (d != 0):
                i -= 1
        else:
            i += 1
    return path

def get_path_from_graph(G):
    G_copy = copy(G)
    # Convert vertices
    extracted = sv.extract_vertices(G_copy)
    new_real_G = sv.replace_vertices(G_copy, extracted)

    G_eul = directed_to_eulerian(new_real_G)
    eulerian_path = get_eulerian_path(G_eul)
    true_path = replace_nodes(new_real_G, eulerian_path)
    sv.replace_vertices_back_in_path(true_path, extracted)

    return true_path