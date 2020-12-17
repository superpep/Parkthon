from PyQt5 import QtWidgets, uic
import database_manager as sqlite
from __manifest__ import path_separator, load_properties, comprobation_message

class Create_patient(QtWidgets.QMainWindow):
    def __init__(self):
        super(Create_patient, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'newPatient.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.newPatientButton.clicked.connect(self.add_patient)
        self.newPatientButton.returnPressed.connect(self.add_patient)
        

    def add_patient(self):
        config = load_properties()
        current_user = config.get('UsersSection', 'currentUser')
        sql_con = sqlite.sqlite_connector()
        if (len(dni) < 9):  # Major que 9 no pot ser perque està controlat a l'interfície
            QtWidgets.QMessageBox.critical(self, 'ERROR', "El DNI debe ser de 9 dígitos.")
        elif (len(passwd) < 1):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "La contraseña no puede estar vacía")
        else:
            try:
                sql_con.add_patient(self.dni.text(), self.nom.text(), self.cognom.text(), current_user)
                QtWidgets.QMessageBox.information(self, 'Paciente añadido', "¡El paciente ha sido añadido con éxito!")
                if comprobation_message('Añadir otro paciente', '¿Quieres añadir otro paciente?'): # If OK is clicked in the button
                    self.dni.setText("")
                    self.nom.setText("")
                    self.cognom.setText("")
                else:
                    self.close()
            except sqlite.sqlite3.IntegrityError:
                QtWidgets.QMessageBox.critical(self, 'ERROR', "Ya existe un usuario con este DNI")
            finally:
                sql_con.close()