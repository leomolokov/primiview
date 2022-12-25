class Buttons():
    def initButtons(self, dxf_data):
        self.dxf_data = dxf_data

        self.openButton.clicked.connect(self.openandshow_dxf)
        self.savelikedxfButton.clicked.connect(self.savelike_dxf)

        # self.drawing_initialize.clicked.connect(self.draw_call)
        #
        # self.ConstSpinButton.stateChanged.connect(self.check_espin)
        # self.transparency_checkBox.stateChanged.connect(self.check_transparency)

    def get_dxf_path(self):
        self.explore_source_path()

    def get_save_dir(self):
        self.set_save_dir()

    def openandshow_dxf(self):
        source_path = self.explore_source_path()
        self.dxf_data.get_primitives_data(source_path)
        self.draw_lines_call()

    def savelike_dxf(self):
        target_path = self.set_save_dir()
        self.dxf_data.print_dxf_into_txt(target_path)