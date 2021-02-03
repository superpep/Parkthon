from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import Qt
from __manifest__ import path_separator
import database_manager as sqlite
import chrono
from edit_observation_dialog import edit_observation_dialog
patient_dni = ""

class Patient_info(QtWidgets.QMainWindow):
    editObservationDialog = None
    patient_dni = None
    def __init__(self, current_user, current_patient):
        super(Patient_info, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi("test"+path_separator+'UI'+path_separator+'patient_info.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.patient_info.setAlignment(QtCore.Qt.AlignCenter)

        self.patient_dni = current_patient
        doctor = current_user

        sql_con = sqlite.sqlite_connector()
        self.patient_info.setText("Paciente: "+sql_con.get_patient_name(doctor, self.patient_dni))        
        
        self.model = TableModel(sql_con.get_patient_times(self.patient_dni))
        sql_con.close()
        self.info_table.setModel(self.model)
        self.info_table.clicked.connect(self.editar)

    def editar(self,item):
        if(item.column() == 5):
            self.editObservationDialog = edit_observation_dialog(item.data(), self.model.getData()[item.row()][0], self.patient_dni)
            print("testestest")
		
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
    