from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import login
import sqlite_connector as sqlite
import chrono

class Users_management(QtWidgets.QMainWindow):
    def __init__(self):
        super(Users_management, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+login.getOsSeparator()+'users.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.cronIcon.clicked.connect(self.return_to_chrono)
        self.show_users()

    def show_users(self):
        model = QtGui.QStandardItemModel()
        self.usersList.setModel(model)
        sql_con = sqlite.sqlite_connector(login.getDB())
        users = sql_con.get_users()
        for user in users:
            row = QtGui.QStandardItem(user[0])
            model.appendRow(row)

        

    def return_to_chrono(self):
        self.new_window = chrono.Chrono()
        self.new_window.show()
        self.close()
        
# Eliminar aço despres de acabar les proves ja que no volem que es puga executar
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Users_management() # Create an instance of our class
    app.exec_() # Start the application