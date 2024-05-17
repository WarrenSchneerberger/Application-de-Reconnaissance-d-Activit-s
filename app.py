import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QTextEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application de Reconnaissance d'Activités")

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        
        self.button_load_data = QPushButton("Charger les Données")
        self.button_load_data.clicked.connect(self.load_data)

        self.button_show_stats = QPushButton("Afficher les Statistiques Descriptives")
        self.button_show_stats.clicked.connect(self.show_stats)

        self.text_stats = QTextEdit()
        self.text_stats.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.button_load_data)
        layout.addWidget(self.button_show_stats)
        layout.addWidget(self.canvas)
        layout.addWidget(self.text_stats)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_data(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Charger les Données", "", "All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            self.data = pd.read_csv(fileName)
            self.visualize_data()

    def visualize_data(self):
        if hasattr(self, 'data'):
            self.canvas.ax.clear()
            self.data.plot(ax=self.canvas.ax)
            self.canvas.draw()

    def show_stats(self):
        if hasattr(self, 'data'):
            stats = self.data.describe()
            self.text_stats.setPlainText(stats.to_string())

    def visualize_results(self):
        if hasattr(self, 'results'):
            self.canvas.ax.clear()
            self.results.plot(ax=self.canvas.ax, kind='bar')
            self.canvas.draw()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
