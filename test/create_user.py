from PyQt5 import QtWidgets, uic
from __manifest__ import path_separator, comprobation_message
import database_manager as sqlite
import user_management


class Create_user(QtWidgets.QMainWindow):
    def __init__(self, first_user=False):
        super(Create_user, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('UI' + path_separator + 'newUser.ui', self)  # Load the .ui file
        self.show()  # Show the GUI

        if(first_user):
            sql_con = sqlite.sqlite_connector()
            sql_con.create_initial_table() # Creem les taules inicials
            sql_con.close()
            self.adminCheck.setChecked(True)
            self.adminCheck.toggled.connect(self.set_true)


        self.newUserButton.clicked.connect(self.create_user)
        self.user.returnPressed.connect(self.create_user)
        self.passwd.returnPressed.connect(self.create_user)
        
    def set_true(self):
        self.adminCheck.setChecked(True)
        QtWidgets.QMessageBox.critical(self, 'Error', "El primer usuario DEBE ser adminisrador") # Mostrem un missatge emergent d'error


    def create_user(self):
        dni = self.user.text()
        passwd = self.passwd.text()
        if (len(dni) < 9):  # Major que 9 no pot ser perque està controlat a l'interfície
            QtWidgets.QMessageBox.critical(self, 'ERROR', "El DNI debe ser de 9 dígitos.")
        elif (len(passwd) < 8):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "La contraseña no puede ser menor a 8 carácteres.")
        else:
            try:
                sql_con = sqlite.sqlite_connector()
                sql_con.create_user(dni, passwd, self.adminCheck.isChecked())
                QtWidgets.QMessageBox.information(self, 'Usuario añadido', "¡El usuario ha sido añadido con éxito!")
                if comprobation_message('Añadir otro usuario', '¿Quieres añadir otro usuario?'): # If OK is clicked in the button
                    self.dni.setText("")
                    self.passwd.setText("")
                else:
                    self.close()
            except sqlite.sqlite3.IntegrityError:
                QtWidgets.QMessageBox.critical(self, 'ERROR', "Ya existe un usuario con este DNI")
            finally:
                self.user.setText("")
                self.passwd.setText("")
                sql_con.close()