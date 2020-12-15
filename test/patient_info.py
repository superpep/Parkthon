from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt
from __manifest__ import path_separator, load_properties
import database_manager as sqlite

class Patient_info(QtWidgets.QMainWindow):
    def __init__(self):
        super(Patient_info, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'patient_info.ui', self) # Load the .ui file
        self.show() # Show the GUI

        config = load_properties()
        self.patient_dni = config.get('PatientsSection', 'selectedPatient')

        sql_con = sqlite.sqlite_connector()
        data = sql_con.get_patient_times(self.patient_dni)


        self.model = TableModel(data)
        self.info_table.setModel(self.model)

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])