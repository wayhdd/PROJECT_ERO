import osmnx as ox

place = "Montreal, Canada" 
G = ox.graph_from_place(place, network_type="walk")
ox.plot_graph(G)