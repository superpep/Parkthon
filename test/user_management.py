from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import login
import database_manager as sqlite
import chrono

class Users_management(QtWidgets.QMainWindow):
    def __init__(self):
        super(Users_management, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+login.pathSeparator+'users.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.deleteUser.clicked.connect(self.delete_user)

        self.model = QtGui.QStandardItemModel()
        self.usersList.setModel(self.model)
        self.sql_con = sqlite.sqlite_connector()
        self.reinicia_llista()
        self.dni = ""

        self.cronIcon.clicked.connect(self.return_to_chrono)
        
        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color: #f0f0f0}")
        self.barraLateral.setStyleSheet("QWidget#barraLateral{ background-color: #d6d6d6; }")
        self.cronIcon.setStyleSheet("QPushButton#cronIcon::hover{ border: none; background-color: #ccdeff;} QPushButton#cronIcon::pressed{background-color: #668BCC;}")
        self.users.setStyleSheet("QPushButton#users::hover{ border: none; background-color: #ccdeff;} QPushButton#users::pressed{background-color: #668BCC;}")

        self.usersList.clicked.connect(self.manage_user)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def manage_user(self, index):
        self.dni = self.model.itemFromIndex(index).text()
        self.changePass.show()
        self.deleteUser.show()

    def delete_user(self):
        print(login.currentUser)
        if login.currentUser == self.dni: # Arreglar aço
            QtWidgets.QMessageBox.critical(self, 'ERROR', "No puedes eliminar tu propio usuario")
        else:
            choice = my_button()
            if choice:
                if(self.sql_con.delete_user(self.dni)):
                    QtWidgets.QMessageBox.information(self, 'Confirmación', "El usuario ha sido eliminado con éxito.")
                    self.reinicia_llista()
                else:
                    QtWidgets.QMessageBox.critical(self, 'ERROR', "El usuario no puede eliminarse porque es el único administrador")
            else:
                pass

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
        
# Eliminar aço despres de acabar les proves ja que no volem que es puga executar
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Users_management() # Create an instance of our class
    app.exec_() # Start the application