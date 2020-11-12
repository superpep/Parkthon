from PyQt5 import QtWidgets, uic
import sqlite_connector as sqlite
import sys


DB = "DB/parkthon.db" # RUTA DE LA BASE DE DADES

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI/login.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.loginButton.clicked.connect(self.algo)

    def algo(self):
        if(sqlite.database_exists(DB)):
            sql_con = sqlite.sqlite_connector(DB)
            if(sql_con.login(self.user.text(), self.passwd.text())):
                self.errorLabel.hide()
                pass
            else:
                self.errorLabel.setText("Error. DNI i/o contrasenya incorrecta")

        else:
            sql_con = sqlite.sqlite_connector(DB)
            sql_con.create_initial_table()
            sql_con.create_user(self.user.text(), self.passwd.text())
            # TO-DO: Implementar aço, no sabem si fer una finestra nova on demanar dades.
        


app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application