from PyQt5 import QtWidgets, uic
import os
pathSeparator = os.path.sep
import sys
import database_manager as sqlite
import chrono
import configparser
from PyQt5.QtCore import QPropertyAnimation, QSize, QAbstractAnimation, QRect

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
                config = configparser.RawConfigParser()
                config.read(sqlite.configFileName)
                config.set('UsersSection', 'currentUser', self.user.text())     
                with open(sqlite.configFileName, 'w') as configfile:
                    config.write(configfile)
                self.open_new_window()
                
            else:
                self.errorLabel.setText("Error. DNI i/o contrasenya incorrecta")

        else:
            sql_con = sqlite.sqlite_connector()
            sql_con.create_initial_table()
            sql_con.create_user(self.user.text(), self.passwd.text(), True)
            # TO-DO: Implementar aço, no sabem si fer una finestra nova on demanar dades.
    
    def open_new_window(self):
        startX = self.x()
        startY = self.y()
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(300)
        self.anim.setStartValue(QRect(startX, startY, 301, 281))
        self.anim.setEndValue(QRect(0, 0, 1366, 768))

        self.fade = QPropertyAnimation(self, b"windowOpacity")
        self.fade.setDuration(300)
        self.fade.setStartValue(1)
        self.fade.setEndValue(0.2)

        self.fade.start()
        self.anim.start()
        self.anim.finished.connect(self.start_login)

    def start_login(self):
        self.new_window = chrono.Chrono()
        self.close()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Ui() # Create an instance of our class
    app.exec_() # Start the application