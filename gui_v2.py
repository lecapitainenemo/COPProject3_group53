import sys
import osmnx as ox

#print('hello world')


import matplotlib
import random

matplotlib.use('Qt5Agg')  
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel
import matplotlib.backends.backend_qt5agg as qt5agg

import math

def dijkstra(dictionary, source, destination):

    path_weight_list = [None for x in range(len(dictionary))]
    prev_vertex_list = [None for x in range(len(dictionary))]

    for idx, val in enumerate(dictionary):

        if source == idx:
            path_weight_list[idx] = 0
        else:
            path_weight_list[idx] = math.inf
        
    verts = list(range(len(dictionary)))
    unvisited_set = set(verts)
    visited_set = set()

    visited_set.add(source)
    unvisited_set.remove(source)

    while(len(unvisited_set) != 0):

        neighbors = dictionary[source]
        
        for neighbor in neighbors:

            if path_weight_list[neighbor] > path_weight_list[source] + neighbors[neighbor]:
                path_weight_list[neighbor] = path_weight_list[source] + neighbors[neighbor]
                prev_vertex_list[neighbor] = source

        min_dist = math.inf

        for unvisited_vert in unvisited_set:
            if path_weight_list[unvisited_vert] < min_dist:
                min_dist = path_weight_list[unvisited_vert]
                source = unvisited_vert

        visited_set.add(source)
        unvisited_set.remove(source)
     
    return path_weight_list[destination]


class MatplotlibApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map Plotter with PyQt5")
        self.setGeometry(100, 100, 800, 600)

        
        central_widget = QWidget()
        layout = QVBoxLayout()

        
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Enter a location (e.g., 'Gainesville, FL')")
        layout.addWidget(self.location_input)

        self.plot_button = QPushButton("Plot Map")
        self.plot_button.clicked.connect(self.plot_map)
        layout.addWidget(self.plot_button)

       
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        
        self.canvas = None

        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def plot_map(self):
        location = self.location_input.text().strip()
        if not location:
            self.status_label.setText("Please enter a location.")
            return
        
        self.status_label.setText("Fetching data...")
        QApplication.processEvents()

        try:
            

            G = ox.graph_from_place(location, network_type='drive')
            #G = ox.graph_from_address('350 5th Ave, New York, New York', network_type='drive')
            fig2 = ox.plot_graph(G)

            G_nodes = list(G.nodes())
            print('xyz: ' + str(G_nodes))
            print('xyz type: ' + str(type(G_nodes)))

            dictionary_original_to_sequential = {}
            for idx, val in enumerate(G_nodes):
                dictionary_original_to_sequential[val] = idx

            #print('graph: ' + str(G[0]))

            dict_all = [(n, nbrdict) for n, nbrdict in G.adjacency()]
            print('num elements: ' + str(len(dict_all)))
            print('element: ' + str(dict_all[0]))
            print('element type: ' + str(type(dict_all[2])))

            first_rand = random.randrange(0, len(dict_all))
            second_rand = random.randrange(0, len(dict_all))

            x = dict_all[0]
            print('first element type: ' + str(type(x[1])))
            print('first element: ' + str(x[1]))
            print('first element keys: ' + str(list(x[1].keys())))

            dict_all_abridged = {}

            print('number of elements in G nodes: ' + str(len(G_nodes)))

            print('first element investigated: ' + str(dict_all[0]))
            print('first element investigated second level: ' + str(dict_all[0][0]))

            for idx, val in enumerate(dict_all):
                
                neighbors_list = []
                length_list = []
                neighbors = list(dict_all[idx][1])

                neighbors_sequential = []
                for neighbor in neighbors:
                    neighbor_sequential = dictionary_original_to_sequential[neighbor]


                d = {}
                for neighbor in neighbors:
                    length = val[1][neighbor][0]['length']
                    #print('value of x: ' + str(x))
                    d[dictionary_original_to_sequential[neighbor]] = length

                dict_all_abridged[idx] = d

                #for neighbor in neighbors:
                #    neighbors_list.append(neighbor)

                #lengths = list(dict_all[idx][1])

                #for x in dict_all:
                    
                #    for neighbor in neighbors:
                #dict_all[val]
                        

                #    pass
                    #neighbor

                if idx == 0:
                    print('neighbors: ' + str(neighbors))
                    print('neighbors list: ' + str(neighbors_list))

                '''
                d = {}
                for j, vals in dict_all[idx]:
                    neighbor = j
                    length = j
                    d[neighbor] = length

                dict_all_abridged[val] = d
                '''



            print('end ======= ')
            print('first dictionary value: ' + str(dict_all_abridged[0]))

                #dict_all_abridged[val] = list(dict_all[idx][1].keys())
                #dict_all_abridged[val] = idx

            print('x0: ' + str(dict_all_abridged[0]))
            print('x1: ' + str(dict_all_abridged[1]))
            print('x2: ' + str(dict_all_abridged[2]))

            #nodes = dict_all.keys()

            route = ox.shortest_path(G, dict_all[0][0], dict_all[5][0])

            #print('source: ' + str(dict_all_abridged[0]))
            #print('destination: ' + str(dict_all_abridged[5]))

            print('source: ' + str(G_nodes[0]))
            print('destination: ' + str(G_nodes[5]))
            print('dictionary: ' + str(dict_all_abridged))

            print('source sequential: ' + str(dictionary_original_to_sequential[G_nodes[0]]))
            print('destination sequential: ' + str(dictionary_original_to_sequential[G_nodes[5]]))

            #route2 = dijkstra(dict_all_abridged, dictionary_original_to_sequential[G_nodes[0]], dictionary_original_to_sequential[G_nodes[5]])
            #route2 = dijkstra(dict_all_abridged, 0, 1)


            print('shortest route: ' + str(route))
            print('shortest route type: ' + str(type(route)))

            fig3, ax3 = ox.plot_graph_route(G, route, route_linewidth=6, node_size=0, bgcolor='k')



            print('first rand: ' + str(first_rand))
            print('second rand: ' + str(second_rand))

            if G.number_of_nodes() == 0:
                self.status_label.setText("No data found for the location.")
                return

            #route = ox.shortest_path(G, dict_all[0], dict_all[0])
            #fig, ax = ox.plot_graph_route(G, route, route_linewidth=6, node_size=0, bgcolor='k')
            
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.set_title(f"Map of {location}")

           
            #ox.plot_graph(G, ax=ax3, show=False, close=False)

            
            if self.canvas:
                self.canvas.figure.clf()
                self.canvas.get_default_target().deleteLater()

            #self.canvas1 = qt5agg.FigureCanvasQTAgg(fig)
            self.canvas3 = qt5agg.FigureCanvasQTAgg(fig3)
            #self.layout().addWidget(self.canvas1)
            self.layout().addWidget(self.canvas3)
            #self.canvas1.draw()
            self.canvas3.draw()

            self.status_label.setText("Map plotted successfully.")

        except Exception as e:
            self.status_label.setText(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatplotlibApp()
    window.show()
    sys.exit(app.exec_())
