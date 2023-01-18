from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5.QtWidgets import QFileDialog

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from ui.main_dialog import Ui_MainWindow
from buttons import Buttons

import os

class MainWindow(QMainWindow, Ui_MainWindow, Buttons):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        fig = Figure()
        axes = fig.add_subplot(111)

        canvas = FigureCanvasQTAgg(fig)
        comp_for_mpl = QVBoxLayout(self.MplWidget)
        comp_for_mpl.addWidget(canvas)

        self.axes = axes
        self.canvas = canvas

        self.initButtons()

    # def check_folder(self, destination):
    #     from pathlib import Path
    #     p = Path('.')
    #     p2 = p / str(destination)
    #     if p2.exists():
    #         p = p2
    #     p = p.absolute()

    def explore_source_path(self):
        from pathlib import Path
        p = Path('.')
        p2 = p / 'test_dxfs'
        if p2.exists():
            p = p2
        p = p.absolute()
        # dir1 = self.check_folder('test_dxfs')
        file_filter = 'Data file (*.dxf)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select dxf to read',
            directory=str(p), #os.getcwd() + '/test_dxfs',
            filter=file_filter
        )
        self.dxfPath = response[0]
        print(self.dxfPath)
        return self.dxfPath


    def set_save_dir(self, type: 'txt' or 'svg'):
        from pathlib import Path
        p = Path('.')
        p2 = p / 'test_dxfs'
        if p2.exists():
            p = p2
        p = p.absolute()
        file_filter = 'Data file (*.' + type +')'
        response = QFileDialog.getSaveFileName(
            self,
            caption='Select a folder',
            directory=str(p), #os.getcwd(),
            filter=file_filter
        )
        # self.txtPath = response[0]
        # print(self.txtPath)
        return response[0]


    def redraw(self):
        self.canvas.draw()
        self.canvas.flush_events()

    def draw_lines_call(self):
        self.sketch.draw_lines(self.axes)
        self.redraw()