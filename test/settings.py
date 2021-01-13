from PyQt5 import QtWidgets, uic, QtGui, QtCore
from __manifest__ import path_separator
import database_manager as sqlite

class Settings(QtWidgets.QMainWindow):
    def __init__(self):
        super(Settings, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'settings.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color: #555860}")
        self.edit_button.setStyleSheet("QPushButton#edit_button{ border-radius: 8px; font-weight: bold; color: #fdfdff; background-color: #222628; } QPushButton#edit_button::hover{ background-color: #383b3d;} QPushButton#edit_button::pressed{background-color: black;}")
        self.show_times()
        self.edit_button.clicked.connect(self.edit_mode)

        self._close_window = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self)
        self._close_window.activated.connect(self.close_window)


    def show_times(self):
        sql_con = sqlite.sqlite_connector()

        self.seg1_max.setText(str(sql_con.get_segment_time("seg1_max_time")))
        self.seg1_min.setText(str(sql_con.get_segment_time("seg1_min_time")))

        self.seg2_max.setText(str(sql_con.get_segment_time("seg2_max_time")))
        self.seg2_min.setText(str(sql_con.get_segment_time("seg2_min_time")))
        
        self.seg3_max.setText(str(sql_con.get_segment_time("seg3_max_time")))
        self.seg3_min.setText(str(sql_con.get_segment_time("seg3_min_time")))

        self.tiempoTotal_max.setText(str(sql_con.get_segment_time("total_max_time")))
        self.tiempoTotal_min.setText(str(sql_con.get_segment_time("total_min_time")))
        sql_con.close()

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
        self.save_data()

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
    
    def save_data(self):
        """
        Desa tots els canvis
        """
        sql_con = sqlite.sqlite_connector()
        times = [float(self.tiempoTotal_min.text()), float(self.tiempoTotal_max.text()), float(self.seg1_min.text()), float(self.seg1_max.text()), float(self.seg2_min.text()), float(self.seg2_max.text()), float(self.seg3_min.text()), float(self.seg3_max.text())]
        sql_con.set_new_segments_time(times)
    
    def close_window(self):
        self.close()