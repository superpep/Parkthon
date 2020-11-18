from PyQt5 import QtWidgets, uic, QtCore, QtGui
#from PyQt5.QtWidgets import QLabel
import sys
import datetime
import user_management
from login import getOsSeparator
from stopwatch import Stopwatch

class Chrono(QtWidgets.QMainWindow):
    def __init__(self):
        super(Chrono, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+getOsSeparator()+'cronometro.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.startStop.clicked.connect(self.start_crono)
        self.lap.clicked.connect(self.record_lap)
        self.users.clicked.connect(self.open_users_menu)

        self.stopwatch = Stopwatch()
        self.stopwatch.stop()
        
        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color: #373A3D}")
        self.barraLateral.setStyleSheet("QWidget#barraLateral{ background-color: #A1A3A5; }")
        self.cronIcon.setStyleSheet("QPushButton#cronIcon::hover{ border: none; background-color: #ccdeff;} QPushButton#cronIcon::pressed{background-color: #668BCC;}")
        self.users.setStyleSheet("QPushButton#users::hover{ border: none; background-color: #ccdeff;} QPushButton#users::pressed{background-color: #668BCC;}")


        self.model = QtGui.QStandardItemModel()
        self.lapsList.setModel(self.model)
    

        self.laps_image = QtGui.QIcon('img/laps.png')
        self.restart_image = QtGui.QIcon('img/restart.png')
        self.start_image = QtGui.QIcon('img/white.png')
        self.pause_image = QtGui.QIcon('img/pause.png')

        self.lap_num = 0
        self.previous_time = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.run_watch)
        self.timer.setInterval(10)
        self.mscounter = 0
        self.isreset = True
        self.showLCD()

    def record_lap(self):
        """
        Afegeix una nova lap al cronómetro
        """
        
        if (self.mscounter > 1000):
            this_time = float(str(self.stopwatch))[:-1]
            self.lap_num += 1
            text = "Lap "+str(self.lap_num)+": "
            if(self.lap_num ==  1):
                text += "{:.2f}".format(this_time)
            else:
                text += "{:.2f}".format(this_time - self.previous_time)
            
            row = QtGui.QStandardItem(text)
            self.previous_time = this_time
            self.model.appendRow(row)


    def showLCD(self):
        """
        Aquesta funció serveix per a mostrar per pantalla el temps
        """
        text = str(datetime.timedelta(milliseconds=self.mscounter))[2:-4]
        if not self.isreset:  # si "isreset" es False
            self.cronNum.setText(str(self.stopwatch))
        else:
            self.cronNum.setText('0.00')

    def run_watch(self):
        """
        Executa el cronómetre de forma interna
        """
        self.mscounter += 10
        self.showLCD()

    def start_crono(self):
        """
        Comença el cronómetre de forma visible
        """
        self.timer.start()
        if(self.stopwatch.running):
            self.stopwatch.restart()
        else:
            self.stopwatch.start()

        self.lap.setIcon(self.laps_image)
        if(self.isreset == False):
            self.lap.clicked.disconnect(self.reset_watch)
            self.lap.clicked.connect(self.record_lap)

        self.startStop.setIcon(self.pause_image)
        self.startStop.clicked.disconnect(self.start_crono)
        self.startStop.clicked.connect(self.pause_watch)
        self.isreset = False
        
    def pause_watch(self):
        """
        Pausa el cronómetre
        """

        self.timer.stop()
        self.stopwatch.stop()


        self.startStop.setIcon(self.start_image)
        self.startStop.clicked.disconnect(self.pause_watch)
        self.startStop.clicked.connect(self.start_crono)

        self.lap.setIcon(self.restart_image)
        self.lap.clicked.disconnect(self.record_lap)
        self.lap.clicked.connect(self.reset_watch)
    
    def reset_watch(self):
        """
        Reinicia el cronómetre
        """
        self.timer.stop()
        self.stopwatch.restart()
        self.mscounter = 0
        self.lap_num = 0
        self.isreset = True
        self.previous_time = 0
        self.showLCD()

        self.startStop.setIcon(self.start_image)



        self.lap.setIcon(self.laps_image)
        self.lap.clicked.disconnect(self.reset_watch)
        self.lap.clicked.connect(self.record_lap)


        self.model.removeRows(0, self.model.rowCount()) # Esborra totes les laps

    def open_users_menu(self):
        self.new_window = user_management.Users_management()
        self.new_window.show()
        self.close()
        

# Eliminar aço despres de acabar les proves ja que no volem que es puga executar
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Chrono() # Create an instance of our class
    app.exec_() # Start the application