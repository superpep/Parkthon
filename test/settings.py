from PyQt5 import QtWidgets, uic
from __manifest__ import path_separator, load_properties, save_property

class Settings(QtWidgets.QMainWindow):
    def __init__(self):
        super(Settings, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'settings.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color: #555860}")
        self.show_times(load_properties())
        self.edit_button.clicked.connect(self.edit_mode)


    def show_times(self, config):
        self.seg1_max.setText(config.get("Seg1TimeSection", "maxiumumtime"))
        self.seg1_min.setText(config.get("Seg1TimeSection", "minimumtime"))

        self.seg2_max.setText(config.get("Seg2TimeSection", "maxiumumtime"))
        self.seg2_min.setText(config.get("Seg2TimeSection", "minimumtime"))
        
        self.seg3_max.setText(config.get("Seg3TimeSection", "maxiumumtime"))
        self.seg3_min.setText(config.get("Seg3TimeSection", "minimumtime"))

        self.tiempoTotal_max.setText(config.get("TotalTimeSection", "maxiumumtime"))
        self.tiempoTotal_min.setText(config.get("TotalTimeSection", "minimumtime"))

    def edit_mode(self):
        """
        Entrem en mode edició
        """
        self.seg1_max.setReadOnly(False)
        self.seg1_min.setReadOnly(False)
        
        self.seg2_max.setReadOnly(False)
        self.seg2_min.setReadOnly(False)
        
        self.seg3_max.setReadOnly(False)
        self.seg3_min.setReadOnly(False)

        self.tiempoTotal_max.setReadOnly(False)
        self.tiempoTotal_min.setReadOnly(False)

        self.edit_button.setText("Guardar")
        self.edit_button.clicked.disconnect(self.edit_mode)
        self.edit_button.clicked.connect(self.save_mode)

    def save_mode(self):
        """
        Tornem al primer mode però guardant els canvis realitzats
        """
        self.save_data(load_properties())

        self.seg1_max.setReadOnly(True)
        self.seg1_min.setReadOnly(True)
        
        self.seg2_max.setReadOnly(True)
        self.seg2_min.setReadOnly(True)
        
        self.seg3_max.setReadOnly(True)
        self.seg3_min.setReadOnly(True)

        self.tiempoTotal_max.setReadOnly(True)
        self.tiempoTotal_min.setReadOnly(True)

        self.edit_button.setText("Editar")
        self.edit_button.clicked.disconnect(self.save_mode)
        self.edit_button.clicked.connect(self.edit_mode)
    
    def save_data(self, config):
        """
        Desa tots els canvis
        """
        save_property("Seg1TimeSection", "maxiumumtime", self.seg1_max.text())
        save_property("Seg1TimeSection", "minimumtime", self.seg1_min.text())

        save_property("Seg2TimeSection", "maxiumumtime", self.seg2_max.text())
        save_property("Seg2TimeSection", "minimumtime", self.seg2_min.text())
        
        save_property("Seg3TimeSection", "maxiumumtime", self.seg3_max.text())
        save_property("Seg3TimeSection", "minimumtime", self.seg3_min.text())

        save_property("TotalTimeSection", "maxiumumtime", self.tiempoTotal_max.text())
        save_property("TotalTimeSection", "minimumtime", self.tiempoTotal_min.text())