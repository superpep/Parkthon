from PyQt5 import QtWidgets, uic
import database_manager as sqlite
from __manifest__ import path_separator, load_properties

class Create_patient(QtWidgets.QMainWindow):
    def __init__(self):
        super(Create_patient, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'newPatient.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.newPatientButton.clicked.connect(self.add_patient)
        self.newPatientButton.returnPressed.connect(self.create_user)
        

    def add_patient(self):
        config = load_properties()
        current_user = config.get('UsersSection', 'current_user')
        sql_con = sqlite.sqlite_connector()
        try:
            sql_con.add_patient(self.dni.text(), self.nom.text(), self.cognom.text(), current_user)
            QtWidgets.QMessageBox.information(self, 'Paciente añadido', "¡El paciente ha sido añadido con éxito!")
            if my_button(): # If OK is clicked in the button
                self.dni.setText("")
                self.nom.setText("")
                self.cognom.setText("")
            else:
                self.close()
        except sqlite.sqlite3.IntegrityError:
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Ya existe un usuario con este DNI")
        finally:
            sql_con.close()

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