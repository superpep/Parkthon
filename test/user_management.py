import create_user
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import login
import database_manager as sqlite
import chrono
import configparser
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QGraphicsOpacityEffect

class Users_management(QtWidgets.QMainWindow):
    def __init__(self):
        super(Users_management, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+login.pathSeparator+'users.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.deleteUser.clicked.connect(self.delete_user)
        self.changePass.clicked.connect(self.change_pass)
        self.newUser.clicked.connect(self.create_user)
        self.refreshList.clicked.connect(self.reinicia_llista)

        config = configparser.RawConfigParser()
        config.read(sqlite.configFileName)
        self.currentUser = config.get('UsersSection', 'currentUser')

        self.model = QtGui.QStandardItemModel()
        self.usersList.setModel(self.model)
        self.usersList.clicked.connect(self.manage_user)

        self.sql_con = sqlite.sqlite_connector()
        self.reinicia_llista()
        self.dni = ""

        if(self.sql_con.is_admin(self.currentUser)):
            self.newUser.show()
        else:
            self.newUser.hide()

        self.cronIcon.clicked.connect(self.return_to_chrono)
        
        
        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color: #f0f0f0}")
        self.barraLateral.setStyleSheet("QWidget#barraLateral{ background-color: #d6d6d6; }")
        self.cronIcon.setStyleSheet("QPushButton#cronIcon::hover{ border: none; background-color: #EEEEEE;} QPushButton#cronIcon::pressed{background-color: #555555;}")
        self.users.setStyleSheet("QPushButton#users::hover{ border: none; background-color: #EEEEEE;} QPushButton#users::pressed{background-color: #555555;}")
        self.pacientesIcon.setStyleSheet("QPushButton#pacientesIcon::hover{ border: none; background-color: #EEEEEE;} QPushButton#pacientesIcon::pressed{background-color: #555555;}")
        

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def manage_user(self, index):
        self.dni = self.model.itemFromIndex(index).text()
        if(self.sql_con.is_admin(self.currentUser) or self.dni == self.currentUser):
            self.changePass.show()
        else:
            self.changePass.hide()    

        if(self.sql_con.is_admin(self.currentUser)):
            self.deleteUser.show()
        else:
            self.deleteUser.hide()

    def create_user(self):
        self.new_window = create_user.Create_user()

    def change_pass(self):
        accesGranted = self.sql_con.is_admin(self.dni)
        if(not accesGranted): # Si no és admin
            last_passwd, ok = QtWidgets.QInputDialog.getText(self, 'Identifícate', 'Introduzca su contraseña actual, '+self.dni)
            if ok:
                if(not self.sql_con.login(self.dni, last_passwd)): # SI L'AUTENTICACIÓ NO ÉS CORRECT
                    QtWidgets.QMessageBox.critical(self, 'ERROR', "Contraseña incorrecta.")
                    return
                else:
                    accesGranted = True
            else:
                return
        if(accesGranted):
            valid_password = False
            while(not valid_password):
                passwd, ok = QtWidgets.QInputDialog.getText(self, 'Cambio de contraseña para usuario '+self.dni, 'Introduzca la nueva contraseña: (8 carácteres o más)')
                if ok:
                    if(len(passwd) < 8):
                        QtWidgets.QMessageBox.critical(self, 'ERROR', "La contraseña debe ser de 8 carácteres o más")
                    else:
                        valid_password = True
                else:
                    return
            self.sql_con.change_password(self.dni, passwd)
            QtWidgets.QMessageBox.information(self, 'Contraseña actualizada', "¡La contraseña ha sido actualizada con éxito!")


    def delete_user(self):
        if self.currentUser == self.dni: # Arreglar aço
            QtWidgets.QMessageBox.critical(self, 'ERROR', "No puedes eliminar tu propio usuario.")
        else:
            choice = my_button()
            if choice:
                if(self.sql_con.delete_user(self.dni)):
                    QtWidgets.QMessageBox.information(self, 'Confirmación', "El usuario ha sido eliminado con éxito.")
                    self.reinicia_llista()
                else:
                    QtWidgets.QMessageBox.critical(self, 'ERROR', "El usuario no puede eliminarse porque es el único administrador.")

    def reinicia_llista(self):
        self.model.removeRows(0, self.model.rowCount()) # Esborra tot
        self.changePass.hide()
        self.deleteUser.hide()
        self.show_users()

    def show_users(self):
        users = self.sql_con.get_users()
        for user in users:
            row = QtGui.QStandardItem(user[0])
            self.model.appendRow(row)

    def return_to_chrono(self):
        self.new_window = chrono.Chrono()
        self.new_window.show()
        self.close()

def my_button():
    box = QtWidgets.QMessageBox()
    box.setIcon(QtWidgets.QMessageBox.Question)
    box.setWindowTitle('Comprovació')
    box.setText('¿Estás seguro de querer eliminar al usuario?')
    box.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
    buttonY = box.button(QtWidgets.QMessageBox.Yes)
    buttonY.setText('Sí')
    buttonN = box.button(QtWidgets.QMessageBox.No)
    buttonN.setText('No')
    box.exec_()
    return box.clickedButton() == buttonY
        
    def lastWindowClosed(self):
        print("Xd")
# Eliminar aço despres de acabar les proves ja que no volem que es puga executar
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Users_management() # Create an instance of our class
    app.exec_() # Start the application