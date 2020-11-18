from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
from login import getOsSeparator

class Users_management(QtWidgets.QMainWindow):
    def __init__(self):
        super(Users_management, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+getOsSeparator()+'users.ui', self) # Load the .ui file
        self.show() # Show the GUI
        
# Eliminar aço despres de acabar les proves ja que no volem que es puga executar
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Users_management() # Create an instance of our class
    app.exec_() # Start the application