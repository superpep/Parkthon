from PyQt5 import QtWidgets, uic
import sys

class Chrono(QtWidgets.QMainWindow):
    def __init__(self):
        super(Chrono, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI/cronometro.ui', self) # Load the .ui file
        self.show() # Show the GUI

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Chrono() # Create an instance of our class
    app.exec_() # Start the application