from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import login
import database_manager as sqlite
import user_management


class Create_user(QtWidgets.QMainWindow):
    def __init__(self):
        super(Create_user, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('UI' + login.pathSeparator + 'newUser.ui', self)  # Load the .ui file
        self.show()  # Show the GUI

        self.newUserButton.clicked.connect(self.create_user)
        self.sql_con = sqlite.sqlite_connector()

    def create_user(self):
        dni = self.user.text()
        passwd = self.passwd.text()
        if (len(dni) < 9):  # Major que 9 no pot ser perque està controlat a l'interfície
            QtWidgets.QMessageBox.critical(self, 'ERROR', "El DNI debe ser de 9 dígitos.")
        elif (len(passwd) < 1):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "La contraseña no puede estar vacía")
        else:
            try:
                self.sql_con.create_user(dni, passwd, self.adminCheck.isChecked())
                QtWidgets.QMessageBox.information(self, 'Paciente añadido', "¡El paciente ha sido añadido con éxito!")
                QtWidgets.QInputDialog.getText(self, '¿Introducir nuevo paciente?', '¿Quieres añadir un otro paciente?')

            except sqlite.sqlite3.IntegrityError:
                QtWidgets.QMessageBox.critical(self, 'ERROR', "Ya existe un usuario con este DNI")
            finally:
                self.user.setText("")
                self.passwd.setText("")
                

    def closeEvent(self, event):
        event.accept()


# Eliminar aço despres de acabar les proves ja que no volem que es puga executar
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    window = Create_user()  # Create an instance of our class
    app.exec_()  # Start the application
