from PyQt5 import QtWidgets, uic, QtGui, QtCore
import database_manager as sqlite
from __manifest__ import path_separator, load_properties, comprobation_message, calculate_imc, photo_to_blob, load_doctors

import sys

class Create_patient(QtWidgets.QMainWindow):
    def __init__(self):
        super(Create_patient, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'newPatient.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.dni_letters = 'TRWAGMYFPDXBNJZSQVHLCKE'

        self.dni.editingFinished.connect(self.calculate_dni_char)
        
        self.fotoCara.setPixmap(QtGui.QPixmap("./img/no_photo.png"))
        self.fotoCuerpo.setPixmap(QtGui.QPixmap("./img/no_photo.png"))
        self.newPatientButton.clicked.connect(self.add_patient)
            
        self.fase.setPlaceholderText("Escala de Hoehn-Yahr")
        self.fase.addItems(["1", "1.5", "2", "2.5", "3", "4", "5"])
        
        self.medicos.setPlaceholderText("Selecciona un médico")
        load_doctors(self.medicos)
        
        self.pes.editingFinished.connect(self.write_imc);
        self.altura.editingFinished.connect(self.write_imc)

        self.cancelarButton.hide()
        self.guardarButton.hide()

        self.fotoCaraButton.clicked.connect(self.set_photo_cara)
        self.fotoCuerpoButton.clicked.connect(self.set_photo_cuerpo)
        
        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color:#555860; color: black; border-radius: 10px; }")
    
    
    def calculate_dni_char(self):
        dni = self.dni.text()
        if(len(dni) == 8 ):
            self.dni.setText(dni+self.dni_letters[int(dni) % 23])

    def write_imc(self):
        self.imc.setText(calculate_imc(self.pes.text(), self.altura.text()))
    

    def set_photo_cara(self):
        image_path = QtWidgets.QFileDialog.getOpenFileName(self, "Abrir imagen", QtCore.QDir.homePath(), "Archivo png (*.png);;Archivo jpg (*.jpg)")
        if (image_path[0] != ""):    
            self.fotoCara.setPixmap(QtGui.QPixmap(image_path[0]))

    def set_photo_cuerpo(self):
        image_path = QtWidgets.QFileDialog.getOpenFileName(self, "Abrir imagen", QtCore.QDir.homePath(), "Archivo png (*.png);;Archivo jpg (*.jpg)")
        if (image_path[0] != ""):
            self.fotoCuerpo.setPixmap(QtGui.QPixmap(image_path[0]))

    def add_patient(self):
        sql_con = sqlite.sqlite_connector()
        if (len(self.dni.text()) < 9):  # Major que 9 no pot ser perque està controlat a l'interfície
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Introduce un DNI válido.")
        elif(self.dni_letters[int(dni[:-1]) % 23] != dni[-1]):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Letra del DNI errónea")
        if(self.nom.text() == ""):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Es obligatorio introducir un nombre.")
        else:
            try:
                sql_con.add_patient(self.dni.text(), self.nom.text(), self.cognom.text(), self.medicos.itemData(self.medicos.currentIndex()), self.direccio.text(),
                                    self.telefon.text(), self.mail.text(), self.sip.text(), self.altura.text(), self.pes.text(),
                                    self.naiximent.text(), self.hombre.isChecked(), self.diagnostic.text(), self.fase.currentIndex(),
                                    self.imc.text(), self.grasa.text(), self.medicacio.toPlainText(), photo_to_blob(self.fotoCara.pixmap()),
                                    photo_to_blob(self.fotoCuerpo.pixmap()))
                QtWidgets.QMessageBox.information(self, 'Paciente añadido', "¡El paciente ha sido añadido con éxito!")
                if comprobation_message('Añadir otro paciente', '¿Quieres añadir otro paciente?'): # If OK is clicked in the button
                    self.dni.setText("")
                    self.nom.setText("")
                    self.cognom.setText("")
                else:
                    self.close()
            except sqlite.sqlite3.IntegrityError:
                QtWidgets.QMessageBox.critical(self, 'ERROR', "Ya existe un paciente con este DNI")
            finally:
                sql_con.close()