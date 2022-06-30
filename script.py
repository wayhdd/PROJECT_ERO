import osmnx as ox
import networkx as nx

G_1 = ox.load_graphml('data/graph.graphml')
G_2 = ox.load_graphml('data/graph2.graphml')
G_3 = ox.load_graphml('data/graph3.graphml')
G_4 = ox.load_graphml('data/graph4.graphml')
G_5 = ox.load_graphml('data/graph5.graphml')
G_6 = ox.load_graphml('data/graph6.graphml')
G_7 = ox.load_graphml('data/graph7.graphml')
G_8 = ox.load_graphml('data/graph8.graphml')
G_9 = ox.load_graphml('data/graph9.graphml')
G_10 = ox.load_graphml('data/graph10.graphml')
G_11 = ox.load_graphml('data/graph11.graphml')
G_12 = ox.load_graphml('data/graph12.graphml')
G_13 = ox.load_graphml('data/graph13.graphml')
G_14 = ox.load_graphml('data/graph14.graphml')
G_15 = ox.load_graphml('data/graph15.graphml')
G_16 = ox.load_graphml('data/graph16.graphml')
G_17 = ox.load_graphml('data/graph17.graphml')
G_18 = ox.load_graphml('data/graph18.graphml')
G_19 = ox.load_graphml('data/graph19.graphml')

L = [G_1, G_2, G_3, G_4, G_5, G_6, G_7, G_8, G_9, G_10, G_11, G_12, G_13, G_14, G_15, G_16, G_17, G_18, G_19]

def decomplexify(graph):
    node_list = graph.edges(data=True)
    to_graph = nx.Graph()
    for node in node_list:
        #Weight
        dist = node[2]["length"]
        one_way = node[2]["oneway"] 
        n1 = node[0]
        n2 = node[1]
        #Oriented graph
        to_graph.add_edge(n1, n2, weight = dist) 
    return to_graph

def to_gnx(graph):
    gnx = nx.Graph()
    for (a,b,c) in graph:
        gnx.add_edge(a,b, weight=c)
    return gnx

def decomplexify_tograph(osmnx):
    node_list = graph.edges(data=True)
    to_graph = []
    for node in node_list:
        #Weight
        dist = node[2]["length"]
        n1 = node[0]
        n2 = node[1]
        #Oriented graph
        to_graph.append(n1, n2, dist)
    return to_graph
    
#print(G_1.edges(data=True))

def edge_to_remove(g):
      
    d1 = nx.edge_betweenness_centrality(g)
    list_of_tuples = d1.items()
    max_edge = ()
    for key, value in sorted(list_of_tuples, key = lambda x:x[1], reverse = True):
        max_edge = key
        break
    
    return max_edge

def girvan_newman(g):
    connect_comp = nx.connected_components(g)
    lena = nx.number_connected_components(g)
    edges = g.edges()
    L_rem = []
    while (lena == 1):
        u, v = edge_to_remove(g)
        L_rem.append((u,v,edges[(u,v)]['weight']))
        g.remove_edge(u, v) 
        connect_comp = nx.connected_components(g)
        lena=nx.number_connected_components(g)
    return (connect_comp, L_rem)

#Return a list of graph_nx witch match the component
def component_to_graph(components, graph_nx):
    graph_list = []
    for component in components[0]:
        graph_list.append(nx.subgraph(graph_nx, component).copy())
    #for (a, b, c) in components[1]:
     #   graph_list[0].add_edge(a,b, weight=c)
    return graph_list 

def split_in_two(graph_nx):
    L = component_to_graph(girvan_newman(graph_nx.copy()), graph_nx)
    R1 = []
    R2 = []
    #Convert to classical representation
    for u in L[0].edges(data=True):
        R1.append((u[0],u[1],u[2]['weight']))
    for u in L[1].edges(data=True):
        R2.append((u[0],u[1],u[2]['weight']))
    return (R1, R2)

def split_in_n(graph_nx):
    count = 1
    sub_graphs = [graph_nx]
    sub_graph_result = [None]
    while (count < 55):
        graph_nx_  =  sub_graphs.pop(0)
        (graph1, graph2) = split_in_two(graph_nx_)
        if (len(graph1) > 0):
            sub_graph_result.append(graph1)
            sub_graphs.append(to_gnx(graph1))
        if (len(graph2) > 0):
            sub_graph_result.append(graph2)
            sub_graphs.append(to_gnx(graph2))
        sub_graph_result.pop(0)
        count += 1
    return sub_graph_result


import pickle



def split_and_save(G, filename):
    sub_graphs = split_in_n(decomplexify(G))
    with open(filename, "wb") as f:
        pickle.dump(sub_graphs, f)

''' POUR REHAN '''
for  i in range(2,6):
    print("i")
    split_and_save(L[i], "data/graph"+str(i)+".txt")

        
''' POUR ARTHUR'''
for  i in range(6,10):
    split_and_save(L[i], "data/graph"+str(i)+".txt")

