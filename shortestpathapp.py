import sys
import osmnx as ox
import networkx as nx
import plotly.graph_objects as go
import heapq
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QLineEdit, QLabel, QComboBox
)

class PlotlyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shortest Path App")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Enter a location (e.g., 'Gainesville, FL')")
        layout.addWidget(self.location_input)

        self.buffer_size_input = QLineEdit()
        self.buffer_size_input.setPlaceholderText("Enter buffer size in meters (e.g., 1000)")
        layout.addWidget(self.buffer_size_input)

        self.algorithm_selector = QComboBox()
        self.algorithm_selector.addItems(["Dijkstra", "Bellman-Ford"])
        layout.addWidget(self.algorithm_selector)

        self.fetch_button = QPushButton("Fetch Data")
        self.fetch_button.clicked.connect(self.fetch_data)
        layout.addWidget(self.fetch_button)

        self.run_button = QPushButton("Run Algorithm")
        self.run_button.clicked.connect(self.run_algorithm)
        self.run_button.setEnabled(False)
        layout.addWidget(self.run_button)

        self.plot_button = QPushButton("Plot Graph")
        self.plot_button.clicked.connect(self.plot_graph)
        self.plot_button.setEnabled(False)
        layout.addWidget(self.plot_button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.canvas = None
        self.G = None
        self.distances = None
        self.parents = None
        self.start_node = None
        self.end_node = None
        self.algorithm = None

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def dijkstra(self, graph, start):
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
                weight = graph[u][neighbor].get('length', 1)
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    parents[neighbor] = u
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances, parents

    def bellman_ford(self, graph, start):
        distances = {node: float('inf') for node in graph.nodes()}
        distances[start] = 0
        parents = {node: None for node in graph.nodes()}

        for _ in range(len(graph.nodes()) - 1):
            for u in graph.nodes():
                for neighbor in graph.neighbors(u):
                    weight = graph[u][neighbor].get('length', 1)
                    if distances[u] + weight < distances[neighbor]:
                        distances[neighbor] = distances[u] + weight
                        parents[neighbor] = u

        for u in graph.nodes():
            for neighbor in graph.neighbors(u):
                weight = graph[u][neighbor].get('length', 1)
                if distances[u] + weight < distances[neighbor]:
                    raise ValueError('Negative cycle detected')

        return distances, parents

    def fetch_data(self):
        location = self.location_input.text().strip()
        buffer_size = self.buffer_size_input.text().strip()

        if not location:
            self.status_label.setText("Please enter a location.")
            return

        if not buffer_size:
            self.status_label.setText("Please enter a buffer size.")
            return

        try:
            buffer_size = float(buffer_size)
        except ValueError:
            self.status_label.setText("Buffer size must be a number.")
            return

        self.status_label.setText("Fetching data...")
        QApplication.processEvents()

        try:
            # Fetch the graph
            self.G = ox.graph_from_place(location, network_type='all', buffer_dist=buffer_size)
            
            if self.G.number_of_nodes() == 0:
                self.status_label.setText("No data found for the location.")
                return

            # Convert to undirected graph
            self.G = nx.Graph(self.G)

            self.status_label.setText("Data fetched successfully.")
            self.run_button.setEnabled(True)

        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def run_algorithm(self):
        if self.G is None:
            self.status_label.setText("No graph data available. Please fetch the data first.")
            return

        algorithm = self.algorithm_selector.currentText()
        if algorithm not in ["Dijkstra", "Bellman-Ford"]:
            self.status_label.setText("Unknown algorithm.")
            return

        nodes = list(self.G.nodes())
        if len(nodes) < 2:
            self.status_label.setText("Not enough nodes to run the algorithm.")
            return

        # Setting up where the path will begin and end
        self.start_node = nodes[0]
        self.end_node = nodes[1]

        try:
            self.algorithm = algorithm

            import time
            start_time = time.time()

            if algorithm == "Dijkstra":
                self.distances, self.parents = self.dijkstra(self.G, self.start_node)
            elif algorithm == "Bellman-Ford":
                self.distances, self.parents = self.bellman_ford(self.G, self.start_node)

            end_time = time.time()

            # Display results
            path_length = self.distances[self.end_node] if self.end_node in self.distances else float('inf')
            num_nodes = len(self.G.nodes())
            self.status_label.setText(
                f"Algorithm: {algorithm}\n"
                f"Time taken: {end_time - start_time:.2f} seconds\n"
                f"Path length: {path_length:.2f}\n"
                f"Number of nodes: {num_nodes}\n"
                f"Start node: {self.start_node}\n"
                f"End node: {self.end_node}"
            )

            self.plot_button.setEnabled(True)

        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def plot_graph(self):
        if self.G is None:
            self.status_label.setText("No graph data available. Please fetch the data first.")
            return

        if self.distances is None or self.parents is None:
            self.status_label.setText("No algorithm has been run. Please run the algorithm first.")
            return

        try:
            # Reconstruct the path
            path = self.reconstruct_path(self.parents, self.start_node, self.end_node)

            # Create a subgraph with only the nodes in the path and a limited number of surrounding nodes
            subgraph_nodes = set(path)
            surrounding_nodes = set()
            max_additional_nodes = 200  # Limit of surrounding nodes to include

            # Collect surrounding nodes connected to the path nodes
            for node in path:
                neighbors = list(self.G.neighbors(node))
                for neighbor in neighbors:
                    if neighbor not in subgraph_nodes and len(surrounding_nodes) < max_additional_nodes:
                        surrounding_nodes.add(neighbor)
                        if len(surrounding_nodes) >= max_additional_nodes:
                            break
                if len(surrounding_nodes) >= max_additional_nodes:
                    break

            # Combine path nodes with surrounding nodes
            subgraph_nodes.update(surrounding_nodes)
            H = self.G.subgraph(subgraph_nodes)

            # Extract node positions
            pos = nx.spring_layout(H, seed=42)

            # Plotly graph
            edge_trace = go.Scatter(
                x=[],
                y=[],
                line=dict(width=0.5, color='#888'),
                hoverinfo='none',
                mode='lines'
            )

            node_trace = go.Scatter(
                x=[],
                y=[],
                text=[],
                mode='markers',
                hoverinfo='text',
                marker=dict(size=10, color='#1f78b4')
            )

            start_node_trace = go.Scatter(
                x=[],
                y=[],
                text=[],
                mode='markers',
                hoverinfo='text',
                marker=dict(size=12, color='green', symbol='circle')
            )

            end_node_trace = go.Scatter(
                x=[],
                y=[],
                text=[],
                mode='markers',
                hoverinfo='text',
                marker=dict(size=12, color='red', symbol='circle')
            )

            for edge in H.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_trace['x'] += (x0, x1, None)
                edge_trace['y'] += (y0, y1, None)

            for node in H.nodes():
                x, y = pos[node]
                node_trace['x'] += (x,)
                node_trace['y'] += (y,)
                
                if node == self.start_node:
                    start_node_trace['x'] += (x,)
                    start_node_trace['y'] += (y,)
                    start_node_trace['text'] += (f"Start: {node}",)

                if node == self.end_node:
                    end_node_trace['x'] += (x,)
                    end_node_trace['y'] += (y,)
                    end_node_trace['text'] += (f"End: {node}",)

            path_edge_trace = go.Scatter(
                x=[],
                y=[],
                line=dict(width=2, color='red'),
                hoverinfo='none',
                mode='lines'
            )

            for u, v in zip(path[:-1], path[1:]):
                x0, y0 = pos[u]
                x1, y1 = pos[v]
                path_edge_trace['x'] += (x0, x1, None)
                path_edge_trace['y'] += (y0, y1, None)

            fig = go.Figure(data=[edge_trace, node_trace, start_node_trace, end_node_trace, path_edge_trace],
                            layout=go.Layout(
                                showlegend=False,
                                xaxis=dict(showgrid=False, zeroline=False),
                                yaxis=dict(showgrid=False, zeroline=False)
                            ))

            fig.show()

            self.status_label.setText("Graph plotted successfully.")

        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def reconstruct_path(self, parents, start, end):
        path = []
        while end is not None:
            path.append(end)
            end = parents.get(end, None)
        path.reverse()
        return path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotlyApp()
    window.show()
    sys.exit(app.exec_())
