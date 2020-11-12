from PyQt5 import QtWidgets, uic
import sys
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('login.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.loginButton.clicked.connect(self.algo)

    def algo(self):
        print(self.user.toPlainText())



app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application