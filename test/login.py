from PyQt5 import QtWidgets, uic
import os
pathSeparator = os.path.sep
import sys
import database_manager as sqlite
import chrono


currentUser = "" # FER AÇO AMB UN ARXIU DE PROPIETATS


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+pathSeparator+'login.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.loginButton.clicked.connect(self.login_button_clicked)
        self.user.returnPressed.connect(self.login_button_clicked)
        self.passwd.returnPressed.connect(self.login_button_clicked)

    def login_button_clicked(self):
        if(sqlite.database_exists()):
            sql_con = sqlite.sqlite_connector()
            if(sql_con.login(self.user.text(), self.passwd.text())):
                currentUser = self.user.text()
                self.open_new_window()
                
            else:
                self.errorLabel.setText("Error. DNI i/o contrasenya incorrecta")

        else:
            sql_con = sqlite.sqlite_connector()
            sql_con.create_initial_table()
            sql_con.create_user(self.user.text(), self.passwd.text(), True)
            # TO-DO: Implementar aço, no sabem si fer una finestra nova on demanar dades.
    
    def open_new_window(self):
        self.new_window = chrono.Chrono()
        self.new_window.show()
        self.close()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Ui() # Create an instance of our class
    app.exec_() # Start the application