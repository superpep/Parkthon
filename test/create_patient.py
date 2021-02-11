from PyQt5 import QtWidgets, uic, QtGui, QtCore
import database_manager as sqlite
from os.path import dirname, realpath, join
from __manifest__ import load_properties, comprobation_message, calculate_imc, photo_to_blob, load_doctors, check_dni
import re 

import sys

class Create_patient(QtWidgets.QMainWindow):
    def __init__(self, doctor):
        super(Create_patient, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(join(dirname(__file__), 'UI/newPatient.ui'), self) # Load the .ui file
        self.showMaximized() # Show the GUI
        self.dni_letters = 'TRWAGMYFPDXBNJZSQVHLCKE'

        self.doctor = doctor

        self.dni.textChanged.connect(self.check_dni)
        
        self.fotoCara.setPixmap(QtGui.QPixmap(join(dirname(__file__), 'img/no_photo.png')))
        self.fotoCuerpo.setPixmap(QtGui.QPixmap(join(dirname(__file__), 'img/no_photo.png')))
        self.newPatientButton.clicked.connect(self.add_patient)
            
        self.fase.setPlaceholderText("Escala de Hoehn-Yahr")
        self.fase.addItems(["1", "1.5", "2", "2.5", "3", "4", "5"])
        
        self.medicos.setPlaceholderText("Selecciona un médico")
        self.medicos = load_doctors(self.medicos, self.doctor)
        
        self.pes.editingFinished.connect(self.write_imc)
        self.altura.editingFinished.connect(self.write_imc)

        self.cancelarButton.hide()
        self.guardarButton.hide()

        self.fotoCaraButton.clicked.connect(self.set_photo_cara)
        self.fotoCuerpoButton.clicked.connect(self.set_photo_cuerpo)
        
        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color:#555860; color: black; border-radius: 10px; }")
    

    def check_mail(self):
        return re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', self.mail.text())
    
    def check_dni(self):
        check_dni(self.dni, self.dni_letters)
    

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
        elif(self.dni_letters[int(self.dni.text()[:-1]) % 23] != self.dni.text()[-1]):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Letra del DNI errónea")
        elif(self.nom.text() == ""):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Es obligatorio introducir un nombre.")
        elif(not self.check_mail):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "El e-mail no és correcto.")
        else:
            try:
                sql_con.add_patient(self.dni.text(), self.nom.text(), self.cognom.text(), self.medicos.currentText(), self.direccio.text(),
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
            except sqlite.sqlite3.IntegrityError as e:
                QtWidgets.QMessageBox.critical(self, 'ERROR', "Ya existe un paciente con este DNI")
                print(e)
            finally:
                sql_con.close()