import pyrosm
import osmnx as ox
import matplotlib
import networkx as nx

# Get filepath to test PBF dataset
# fp = pyrosm.get_data("mapfinal")
fp = "mapfinal.osm.pbf"
print("Filepath to test data:", fp)

# Initialize the OSM object
osm_object = pyrosm.OSM(fp)

# Get all walkable roads and the nodes
nodes, edges = osm_object.get_network(nodes=True)

# Check first rows in the edge
print(edges.head())

# Create NetworkX graph
networkx_graph = osm_object.to_graph(nodes, edges, graph_type="networkx")

matplotlib.use('Qt5Agg')

# Plot the graph with OSMnx
# ox.plot_graph(networkx_graph)

source_node = ox.get_nearest_node(networkx_graph, (-23.32651, -51.20177))
target_node = ox.get_nearest_node(networkx_graph, (-23.32722, -51.19526))

route = nx.shortest_path(networkx_graph, source_node, target_node, weight="length")
fig, ax = ox.plot_graph_route(networkx_graph, route, route_linewidth=6, node_size=0, bgcolor='k')
