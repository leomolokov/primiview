from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5.QtWidgets import QFileDialog

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from ui.main_dialog import Ui_MainWindow
from buttons import Buttons

import os

class MainWindow(QMainWindow, Ui_MainWindow, Buttons):
    def __init__(self):
        from filedata import DxfData
        from scene import Sketch

        QMainWindow.__init__(self)
        self.setupUi(self)

        self.dxf_data = DxfData()
        self.sketch = Sketch()

        # self.data = data
        # self.orig_data = data.copy()

        fig = Figure()
        axes = fig.add_subplot(111)

        canvas = FigureCanvasQTAgg(fig)
        comp_for_mpl = QVBoxLayout(self.MplWidget)
        comp_for_mpl.addWidget(canvas)

        self.axes = axes
        self.canvas = canvas

        self.initButtons(self.dxf_data)


    def explore_source_path(self):
        file_filter = 'Data file (*.dxf)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select dxf to read',
            directory=os.getcwd(),
            filter=file_filter
        )
        self.dxfPath = response[0]
        print(self.dxfPath)
        return self.dxfPath


    def set_save_dir(self):
        file_filter = 'Data file (*.txt)'
        response = QFileDialog.getSaveFileName(
            self,
            caption='Select a folder',
            directory=os.getcwd(),
            filter=file_filter
        )
        self.txtPath = response[0]
        print(self.txtPath)
        return self.txtPath


    def redraw(self):
        self.canvas.draw()
        self.canvas.flush_events()

    def draw_lines_call(self):
        self.sketch.draw_lines(self.axes)
        self.redraw()