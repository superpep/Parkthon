from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import login
import database_manager as sqlite
import chrono

class Users_management(QtWidgets.QMainWindow):
    def __init__(self):
        super(Users_management, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+login.getOsSeparator()+'users.ui', self) # Load the .ui file
        self.show() # Show the GUI
        
        self.changePass.hide()
        self.deleteUser.hide()

        self.model = QtGui.QStandardItemModel()
        self.usersList.setModel(self.model)

        self.cronIcon.clicked.connect(self.return_to_chrono)
        self.show_users()
        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color: #f0f0f0}")
        self.barraLateral.setStyleSheet("QWidget#barraLateral{ background-color: #d6d6d6; }")
        self.cronIcon.setStyleSheet("QPushButton#cronIcon::hover{ border: none; background-color: #ccdeff;} QPushButton#cronIcon::pressed{background-color: #668BCC;}")
        self.users.setStyleSheet("QPushButton#users::hover{ border: none; background-color: #ccdeff;} QPushButton#users::pressed{background-color: #668BCC;}")

        self.usersList.clicked.connect(self.manage_user)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def manage_user(self, index):
        dni = self.model.itemFromIndex(index).text()
        self.changePass.show()
        self.deleteUser.show()

    def show_users(self):
        
        sql_con = sqlite.sqlite_connector()
        users = sql_con.get_users()
        for user in users:
            row = QtGui.QStandardItem(user[0])
            self.model.appendRow(row)

        

    def return_to_chrono(self):
        self.new_window = chrono.Chrono()
        self.new_window.show()
        self.close()
        
# Eliminar aço despres de acabar les proves ja que no volem que es puga executar
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Users_management() # Create an instance of our class
    app.exec_() # Start the application