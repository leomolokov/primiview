class Buttons():
    def initButtons(self):
        # self.dxf_data = dxf_data

        self.openButton.clicked.connect(self.openandshow_dxf)
        self.savelikedxfButton.clicked.connect(self.savelike_dxf)
        self.cncsaveButton.clicked.connect(self.savelike_prims)
        self.svgsaveButton.clicked.connect(self.savelike_svg)

    def openandshow_dxf(self):
        from filedata import DxfData
        from scene import Sketch

        # source_path = self.explore_source_path()
        # self.dxf_data.get_primitives_data(source_path)

        self.dxf_data = DxfData()
        self.sketch = Sketch()
        self.sketch.initSketch(self.dxf_data)
        self.dxf_data.get_primitives_data(self.explore_source_path())
        self.draw_lines_call()

    def savelike_dxf(self):
        # if 'target_path' not in globals():
        # target_path = self.set_save_dir()
        # self.dxf_data.print_dxf_into_txt(self.dxf_data.target_path)
        self.dxf_data.print_dxf_into_txt(self.set_save_dir())

    def savelike_prims(self):
        self.dxf_data.print_prims_into_txt(self.set_save_dir())
        # self.dxf_data.print_prims_into_txt(if not hasattr(self, 'self.txtPath'): self.set_save_dir())

    def savelike_svg(self):
        self.dxf_data.saveas_svg(self.set_save_dir())