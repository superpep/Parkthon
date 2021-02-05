from PyQt5 import QtWidgets, uic, QtCore, QtGui
from os.path import dirname, join
from PyQt5.QtWidgets import QDialog
import database_manager as sqlite

class edit_observation_dialog(QtWidgets.QDialog):
    def __init__(self, cellContent, date, patient):
        super(edit_observation_dialog, self).__init__()
        uic.loadUi(join(dirname(__file__), 'UI/EditObservationDialog.ui'), self)
        self.setWindowTitle("Editar Observaciones")
        self.date = date
        self.patient = patient
        self.pushButtonAccept.clicked.connect(self.edit)
        self.textEditObservaciones.setText(cellContent)

    def edit(self):
        sql_con = sqlite.sqlite_connector()
        sql_con.edit_observations(self.patient,self.textEditObservaciones.toPlainText(),self.date)
        sql_con.close()
        self.hide()