import pyrosm
import osmnx
from Structures import *
import matplotlib
import networkx as nx

# Preprocessing

# Initialize data
osm_object = pyrosm.OSM("mapfinal.osm.pbf")

# Get all walkable roads and the nodes
nodes, edges = osm_object.get_network(nodes=True)

# Create NetworkX graph
networkx_graph = osm_object.to_graph(nodes, edges, graph_type="networkx")

# Convert to array
node_values = nodes.to_numpy()
edge_values = edges.to_numpy()

nodes_list = []
for node in node_values:
    # id_number, lat, long
    node_object = Node(node[6], node[0], node[1])
    nodes_list.append(node_object)

for edge in edge_values:
    # node1 id_number
    node1 = get_node_from_list(nodes_list, edge[24])
    # node2 id_number
    node2 = get_node_from_list(nodes_list, edge[25])
    node1.insert_adj(node2)
    node2.insert_adj(node1)


# A* Implementation

def heuristic(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(start, goal):
    frontier = PriorityQueue()
    frontier.insert(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start.id_number] = None
    cost_so_far[start.id_number] = 0

    while not frontier.is_empty():
        current = frontier.pop()
        print('Current node: ', current.id_number, 'lat: ', current.lat, 'long: ', current.long)

        if current.id_number == goal.id_number:
            print('Current node id: ', current.id_number, 'Goal node id:', goal.id_number)
            break

        for next in current.adj:
            new_cost = cost_so_far[current.id_number] + heuristic(current.lat, current.long, next.lat, next.long)
            if next.id_number not in cost_so_far or new_cost < cost_so_far[next.id_number]:
                cost_so_far[next.id_number] = new_cost
                priority = new_cost + heuristic(next.lat, next.long, goal.lat, goal.long)
                frontier.insert(next, priority)
                came_from[next.id_number] = current
    return came_from, cost_so_far


# Main loop

# Initial node
source_node = osmnx.get_nearest_node(networkx_graph, (-23.32651, -51.20177))

# Final node
target_node = osmnx.get_nearest_node(networkx_graph, (-23.32722, -51.19526))

start_node = get_node_from_list(nodes_list, source_node)  # NodeObject
goal_node = get_node_from_list(nodes_list, target_node)

came_from, cost_so_far = a_star_search(start_node, goal_node)

reconstructed_path = [target_node]
current = came_from[target_node]
while not current.id_number == source_node:
    reconstructed_path.append(current.id_number)
    current = came_from[current.id_number]
reconstructed_path.append(source_node)

matplotlib.use('Qt5Agg')

# Create NetworkX graph
networkx_graph = osm_object.to_graph(nodes, edges, graph_type="networkx")

fig, ax = osmnx.plot_graph_route(networkx_graph, reconstructed_path, route_linewidth=6, node_size=0, bgcolor='k')

route = nx.shortest_path(networkx_graph, source_node, target_node, weight="length")
fig, ax = osmnx.plot_graph_route(networkx_graph, route, route_linewidth=6, node_size=0, bgcolor='k')