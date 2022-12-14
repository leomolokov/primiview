class Buttons():
    def initButtons(self, dxf_data):
        self.dxf_data = dxf_data

        self.actionExplore.triggered.connect(self.get_dxf_path)
        self.actionSaveTo.triggered.connect(self.get_save_dir)

        self.convertionButton.clicked.connect(self.convert_dxf)
        self.checkdrawingButton.clicked.connect(self.draw_current)
        # self.drawing_initialize.clicked.connect(self.draw_call)
        #
        # self.ConstSpinButton.stateChanged.connect(self.check_espin)
        # self.transparency_checkBox.stateChanged.connect(self.check_transparency)

    def get_dxf_path(self):
        self.explore_source_path()

    def get_save_dir(self):
        self.set_save_dir()

    def convert_dxf(self):
        source_path = self.explore_source_path()
        target_path = self.set_save_dir()
        self.dxf_data.get_primitives_data(source_path, target_path)
        self.dxf_data.print_data_into_txt()

    def draw_current(self):
        self.draw_lines_call()