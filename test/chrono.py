from PyQt5 import QtWidgets, uic, QtCore, QtGui
#from PyQt5.QtWidgets import QLabel
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
    

        self.pauseImage = QtGui.QIcon('img/pause.png')
        self.start_image = QtGui.QIcon('img/white.png')
        self.pause_image = QtGui.QIcon('img/pause.png')

        self.lap_num = 0
        self.previous_time = 0
        self.paused = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.run_watch)
        self.timer.setInterval(1)
        self.mscounter = 0
        self.isreset = True
        self.showLCD() 

    def record_lap(self):
        
        this_time = datetime.timedelta(milliseconds=self.mscounter)
        self.lap_num += 1
        text = "Lap "+str(self.lap_num)+": "
        if (not this_time == "0:00"):
            if(self.lap_num ==  1):
                text += str(this_time)[2:-3]
            else:
                text += str(this_time - self.previous_time)[2:-3]
            
            self.previous_time = this_time
            self.lapsLayout.addWidget(QtWidgets.QLabel(text))


    def showLCD(self):
        text = str(datetime.timedelta(milliseconds=self.mscounter))[:-3]
        self.cronNum.setDigitCount(8)
        if not self.isreset:  # si "isreset" es False
            self.cronNum.display(text)
        else:
            self.cronNum.display('0:00.000')

    def run_watch(self):
        self.mscounter += 1
        self.showLCD()

    def start_crono(self):
        self.timer.start()
        

        self.lap.setText("Lap")
        if(self.isreset == False):
            self.lap.clicked.disconnect(self.reset_watch)
            self.lap.clicked.connect(self.record_lap)

        self.startStop.setIcon(self.pause_image)
        self.startStop.clicked.disconnect(self.start_crono)
        self.startStop.clicked.connect(self.pause_watch)
        self.isreset = False
        
    def pause_watch(self):
        self.timer.stop()

        self.startStop.setIcon(self.start_image)
        self.startStop.clicked.disconnect(self.pause_watch)
        self.startStop.clicked.connect(self.start_crono)

        self.lap.setText("Reset")
        self.lap.clicked.disconnect(self.record_lap)
        self.lap.clicked.connect(self.reset_watch)
    
    def reset_watch(self):
        self.timer.stop()
        self.mscounter = 0
        self.isreset = True
        self.previous_time = 0
        self.showLCD()

        self.startStop.setIcon(self.start_image)



        self.lap.setText("Lap")
        self.lap.clicked.disconnect(self.reset_watch)
        self.lap.clicked.connect(self.record_lap)
        

# Eliminar aço despres de acabar les proves ja que no volem que es puga executar
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Chrono() # Create an instance of our class
    app.exec_() # Start the application