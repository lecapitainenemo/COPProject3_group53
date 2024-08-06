import osmnx as ox
import networkx as nx
import heapq
import matplotlib.pyplot as plt

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start] = 0
    priority_queue = [(0, start)]
    parents = {node: None for node in graph.nodes()}
    visited = set()

    while priority_queue:
        current_distance, u = heapq.heappop(priority_queue)

        if u in visited:
            continue

        visited.add(u)

        for neighbor in graph.neighbors(u):
            weight = graph[u][neighbor].get('length', 1)  # Use 'length' as weight if available
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parents[neighbor] = u
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, parents

def reconstruct_path(parents, start, end):
    path = []
    while end is not None:
        path.append(end)
        end = parents[end]
    path.reverse()
    return path


G = ox.graph_from_place("University of Florida, Gainesville, FL", network_type='all')

G = nx.DiGraph(G)

# Example visualization. Doesnt look pretty-more like a hairballl
start_node = list(G.nodes)[0]  
end_node = list(G.nodes)[1]    
distances, parents = dijkstra(G, start_node)


print(f"Distance from {start_node} to {end_node}: {distances[end_node]}")


path = reconstruct_path(parents, start_node, end_node)
print(f"Shortest path from {start_node} to {end_node}: {path}")


plt.figure(figsize=(15, 15))

pos = nx.kamada_kawai_layout(G)  

nx.draw_networkx_nodes(G, pos, node_size=10, node_color='lightblue')
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray', alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=5, font_family='sans-serif')

path_edges = list(zip(path, path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2, alpha=0.7)
nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='yellow', node_size=50)

plt.title("Shortest Path Highlighted")
plt.show()
