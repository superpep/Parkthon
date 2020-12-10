from PyQt5 import QtWidgets, uic
import database_manager as sqlite
import chrono
from __manifest__ import path_separator, create_properties, load_properties, CONFIG_FILE_NAME, file_exists
from PyQt5.QtCore import QPropertyAnimation, QSize, QAbstractAnimation, QRect


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'login.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.loginButton.clicked.connect(self.login_button_clicked)
        self.user.returnPressed.connect(self.login_button_clicked)
        self.passwd.returnPressed.connect(self.login_button_clicked)
        if(not file_exists(CONFIG_FILE_NAME)):
        	create_properties()

    def login_button_clicked(self):
        sql_con = sqlite.sqlite_connector()
        if(sql_con.get_con() == None):
            sql_con.create_initial_table()
            sql_con.create_user(self.user.text(), self.passwd.text(), True)
            sql_con.close()
            self.load_new_window()

        if(sql_con.login(self.user.text(), self.passwd.text())):
            sql_con.close()
            self.load_new_window()        
        else:
            self.errorLabel.setText("Error. DNI i/o contraseña incorrecta.")
        
        
    def load_new_window(self):
        config = load_properties()
        config.set('UsersSection', 'currentUser', self.user.text())     
        with open(CONFIG_FILE_NAME, 'w') as configfile:
            config.write(configfile)
        self.open_new_window()

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
