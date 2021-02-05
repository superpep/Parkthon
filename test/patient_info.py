from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QToolBar, QTableView
from os.path import dirname, join
import database_manager as sqlite
import chrono
from edit_observation_dialog import edit_observation_dialog

patient_dni = ""

class Patient_info(QtWidgets.QMainWindow):
    editObservationDialog = None
    patient_dni = None
    times_changed = pyqtSignal()

    def __init__(self, current_user, current_patient):
        super(Patient_info, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi(join(dirname(__file__), 'UI/patient_info.ui'), self)  # Load the .ui file
        self.show()  # Show the GUI
        self.patient_info.setAlignment(QtCore.Qt.AlignCenter)

        # Joan C.

        # Declaraciones, no hacen nada solo es para que el Pycharm me ayude.
        self.info_table: QTableView = self.info_table
        self.model: TableModel = ...
        self.current_index: int = -1


        minus_icon = QIcon(join(dirname(__file__), 'img/minus-icon-png-8.jpg'))
        self.delete_selected_test: QAction = self.delete_selected_test
        self.delete_selected_test.setIcon(minus_icon)
        toolbar = QToolBar()
        toolbar.addAction(self.delete_selected_test)
        self.addToolBar(toolbar)
        self.delete_selected_test.setEnabled(False)
        self.delete_selected_test.triggered.connect(self.delete_test)
        # Añadimos un toolbar con una accion y un icono.
        ## Fin


        self.patient_dni = current_patient
        self.doctor = current_user


        self.refresh_table()

        
    def on_table_click(self, item, *args): # He cambiado el nombre de esta funcion para ser mas autodescriptivo.
        self.current_index = item.row()
        if item.column() == 5:
            editObservationDialog = edit_observation_dialog(item.data(), self.model.getData()[self.current_index][0], self.patient_dni)
            editObservationDialog.exec()
            self.refresh_table()
        if self.model.getData()[self.current_index][0] != "N/A":
            self.delete_selected_test.setEnabled(True)

    def delete_test(self):
        if self.current_index != -1:
            sql_con = sqlite.sqlite_connector()
            sql_con.delete_test(self.model.getData()[self.current_index][0], self.patient_dni)
            self.current_index = -1
            self.delete_selected_test.setEnabled(False)
            self.times_changed.emit()
            self.refresh_table()
        else:
            print("Error muffled by delete_test function in chrono.py.")


    def refresh_table(self):
        sql_con = sqlite.sqlite_connector()
        self.patient_info.setText("Paciente: "+sql_con.get_patient_name(self.doctor, self.patient_dni))
        self.model = TableModel(sql_con.get_patient_times(self.patient_dni))
        sql_con.close()
        self.info_table.setModel(self.model)
        self.info_table.clicked.connect(self.on_table_click)



class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        
        self.horizontalHeaders = [''] * 7

        self.setHeaderData(0, Qt.Horizontal, "Fecha y hora")
        self.setHeaderData(1, Qt.Horizontal, "Tiempo total")
        self.setHeaderData(2, Qt.Horizontal, "Segmento 1")
        self.setHeaderData(3, Qt.Horizontal, "Segmento 2")
        self.setHeaderData(4, Qt.Horizontal, "Segmento 3")
        self.setHeaderData(5, Qt.Horizontal, "Observaciones")
        self.setHeaderData(6, Qt.Horizontal, "ID Segmentos")

        
        
        if(data):
            self._data = data
        else:
            default_data = [["N/A"]]
            for i in range(0, 5):
                default_data[0].append("N/A")
            self._data = default_data
            
    def getData(self):
        return self._data

    def setHeaderData(self, section, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            try:
                self.horizontalHeaders[section] = data
                return True
            except:
                return False
        return super().setHeaderData(section, orientation, data, role)
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                return self.horizontalHeaders[section]
            except:
                pass
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            
            return self._data[index.row()][index.column()]
        
        if role == Qt.DecorationRole:
            value = self._data[index.row()][index.column()]
            if(value != "N/A"):
                try:
                    lap_type = chrono.get_lap_type(index.column()-2, value, self._data[index.row()][len(self._data[index.row()])-1])
                    color = chrono.get_color_type(lap_type) 
                    return QtGui.QColor(color)
                except TypeError as e:
                    pass
            

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])
    