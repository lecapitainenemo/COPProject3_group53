import sys
import osmnx as ox
import matplotlib
matplotlib.use('Qt5Agg')  
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel
import matplotlib.backends.backend_qt5agg as qt5agg

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
            
            G = ox.graph_from_place(location, network_type='all')
            if G.number_of_nodes() == 0:
                self.status_label.setText("No data found for the location.")
                return


           
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.set_title(f"Map of {location}")

           
            ox.plot_graph(G, ax=ax, show=False, close=False)

            
            if self.canvas:
                self.canvas.figure.clf()
                self.canvas.get_default_target().deleteLater()

            self.canvas = qt5agg.FigureCanvasQTAgg(fig)
            self.layout().addWidget(self.canvas)
            self.canvas.draw()

            self.status_label.setText("Map plotted successfully.")

        except Exception as e:
            self.status_label.setText(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatplotlibApp()
    window.show()
    sys.exit(app.exec_())
