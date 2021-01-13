from PyQt5 import QtWidgets, uic, QtGui, QtCore
import database_manager as sqlite
from __manifest__ import path_separator, load_properties, comprobation_message, calculate_imc

import sys

class Create_patient(QtWidgets.QMainWindow):
    def __init__(self):
        super(Create_patient, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'newPatient.ui', self) # Load the .ui file
        self.show() # Show the GUI

        
        self.fotoCuerpoPixmap = self.fotoCaraPixmap = MyPixmap("./img/no_photo.png")
        self.fotoCara.setPixmap(self.fotoCaraPixmap)
        self.fotoCuerpo.setPixmap(self.fotoCaraPixmap)
        self.newPatientButton.clicked.connect(self.add_patient)
            
        self.fase.setPlaceholderText("Escala de Hoehn-Yahr")
        self.fase.addItem("1")
        self.fase.addItem("1.5")
        self.fase.addItem("2")
        self.fase.addItem("2.5")
        self.fase.addItem("3")
        self.fase.addItem("4")
        self.fase.addItem("5")
        
        self.pes.editingFinished.connect(self.write_imc);
        self.altura.editingFinished.connect(self.write_imc)

        self.fotoCaraButton.clicked.connect(self.set_photo_cara)
        self.fotoCuerpoButton.clicked.connect(self.set_photo_cuerpo)
        
        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color:#555860; color: black; border-radius: 10px; }")
    
    

    def write_imc(self):
        self.imc.setText(calculate_imc(self.pes.text(), self.altura.text()))
        self.grasa.setText(self.imc.text()+"%")
    

    def set_photo_cara(self):
        image_path = QtWidgets.QFileDialog.getOpenFileName(self, "Abrir imagen", QtCore.QDir.homePath(), "Archivo png (*.png);;Archivo jpg (*.jpg)")
        if (image_path[0] != ""):    
            self.fotoCaraPixmap = MyPixmap(image_path[0])
            self.fotoCara.setPixmap(self.fotoCaraPixmap)

    def set_photo_cuerpo(self):
        image_path = QtWidgets.QFileDialog.getOpenFileName(self, "Abrir imagen", QtCore.QDir.homePath(), "Archivo png (*.png);;Archivo jpg (*.jpg)")
        if (image_path[0] != ""):
            self.fotoCuerpoPixmap = MyPixmap(image_path[0])
            self.fotoCuerpoButton.setPixmap(self.fotoCuerpoPixmap)

    def add_patient(self):
        config = load_properties()
        current_user = config.get('UsersSection', 'currentUser')
        sql_con = sqlite.sqlite_connector()
        if (len(self.dni.text()) < 9):  # Major que 9 no pot ser perque està controlat a l'interfície
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Introduce un DNI válido.")
        if(self.nom.text() == ""):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Es obligatorio introducir un nombre.")
        else:
            try:
                sql_con.add_patient(self.dni.text(), self.nom.text(), self.cognom.text(), current_user, self.direccio.text(),
                                    self.telefon.text(), self.mail.text(), self.sip.text(), self.altura.text(), self.pes.text(),
                                    self.naiximent.text(), self.hombre.isChecked(), self.diagnostic.text(), self.fase.currentIndex(),
                                    self.imc.text(), self.grasa.text(), self.medicacio.text(), self.photoToBlob(self.fotoCaraPixmap.getPath()),
                                    self.photoToBlob(self.fotoCuerpoPixmap.getPath()))
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

    def photoToBlob(self, filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

class MyPixmap(QtGui.QPixmap):
    def __init__(self, path):
        super(MyPixmap, self).__init__(path)
        self._path = path
    def getPath(self):
        return self._path
    



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Create_patient()# Llancem el login
    app.exec_() # Start the application