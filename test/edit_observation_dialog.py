from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QDialog
from __manifest__ import path_separator
import database_manager as sqlite

class edit_observation_dialog(QtWidgets.QDialog):
    def __init__(self, cellContent, date, patient):
        super(edit_observation_dialog, self).__init__()
        uic.loadUi("test"+path_separator+'UI'+path_separator+'EditObservationDialog.ui', self)
        self.setWindowTitle("Editar Observaciones")
        self.date = date
        self.patient = patient
        self.pushButtonAccept.clicked.connect(self.edit)
        self.textEditObservaciones.setText(cellContent)
        self.show()

    def edit(self):
        sql_con = sqlite.sqlite_connector()
        sql_con.edit_observations(self.patient,self.textEditObservaciones.toPlainText(),self.date)
        sql_con.close()
        self.hide()