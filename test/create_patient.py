from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import login
import database_manager as sqlite
import configparser

class Create_patient(QtWidgets.QMainWindow):
    def __init__(self):
        super(Create_patient, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+login.pathSeparator+'newPatient.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.newPatientButton.clicked.connect(self.addPatient)
        

    def addPatient(self):
        config = configparser.RawConfigParser()
        config.read(sqlite.configFileName)
        currentUser = config.get('UsersSection', 'currentUser')
        sql_con = sqlite.sqlite_connector()
        try:
            sql_con.addPatient(self.dni.text(), self.nom.text(), self.cognom.text(), currentUser)
            QtWidgets.QMessageBox.information(self, 'Paciente añadido', "¡El paciente ha sido añadido con éxito!")
            choice = my_button()
            if choice:
                self.dni.setText("")
                self.nom.setText("")
                self.cognom.setText("")
            else:
                self.close()
        except sqlite.sqlite3.IntegrityError:
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Ya existe un usuario con este DNI")


def my_button():
    box = QtWidgets.QMessageBox()
    box.setIcon(QtWidgets.QMessageBox.Question)
    box.setWindowTitle('Añadir otro paciente')
    box.setText('¿Quieres añadir otro paciente?')
    box.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
    buttonY = box.button(QtWidgets.QMessageBox.Yes)
    buttonY.setText('Sí')
    buttonN = box.button(QtWidgets.QMessageBox.No)
    buttonN.setText('No')
    box.exec_()
    return box.clickedButton() == buttonY
# Esborrar aço al acabar proves
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Create_patient() # Create an instance of our class
    app.exec_() # Start the application