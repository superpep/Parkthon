from PyQt5 import QtWidgets, uic
from __manifest__ import path_separator
import database_manager as sqlite
import user_management


class Create_user(QtWidgets.QMainWindow):
    def __init__(self):
        super(Create_user, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('UI' + path_separator + 'newUser.ui', self)  # Load the .ui file
        self.show()  # Show the GUI

        self.newUserButton.clicked.connect(self.create_user)
        self.newUserButton.returnPressed.connect(self.create_user)
        

    def create_user(self):
        dni = self.user.text()
        passwd = self.passwd.text()
        if (len(dni) < 9):  # Major que 9 no pot ser perque està controlat a l'interfície
            QtWidgets.QMessageBox.critical(self, 'ERROR', "El DNI debe ser de 9 dígitos.")
        elif (len(passwd) < 1):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "La contraseña no puede estar vacía")
        else:
            try:
                sql_con = sqlite.sqlite_connector()
                sql_con.create_user(dni, passwd, self.adminCheck.isChecked())
                QtWidgets.QMessageBox.information(self, 'Paciente añadido', "¡El paciente ha sido añadido con éxito!")
                QtWidgets.QInputDialog.getText(self, '¿Introducir nuevo paciente?', '¿Quieres añadir un otro paciente?')

            except sqlite.sqlite3.IntegrityError:
                QtWidgets.QMessageBox.critical(self, 'ERROR', "Ya existe un usuario con este DNI")
            finally:
                self.user.setText("")
                self.passwd.setText("")
                sql_con.close()
