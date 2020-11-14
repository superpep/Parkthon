from PyQt5 import QtWidgets, uic, QtCore
import sys
import datetime
import time

class Chrono(QtWidgets.QMainWindow):
    def __init__(self):
        super(Chrono, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI/cronometro.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.startStop.clicked.connect(self.start_crono)
        self.lap.clicked.connect(self.record_lap)


        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.run_watch)
        self.timer.setInterval(1)
        self.mscounter = 0
        self.isreset = True

    def record_lap(self):
        print(self.cronNum.text())

    def showLCD(self):
        text = str(datetime.timedelta(milliseconds=self.mscounter))[:-3]
        self.cronNum.setDigitCount(8)
        if not self.isreset:  # if "isreset" is False
            self.cronNum.display(text)
        else:
            self.cronNum.display('00:00.000')

    def run_watch(self):
        self.mscounter += 1
        self.showLCD()

    def start_crono(self):
        self.timer.start()
        self.isreset = False
        self.startStop.clicked.connect(self.stop_watch)
    
    def stop_watch(self):
        self.timer.stop()
        self.mscounter = 0
        self.cronNum.display('00:00.000')
        self.startStop.clicked.connect(self.start_crono)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Chrono() # Create an instance of our class
    app.exec_() # Start the application