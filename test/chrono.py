from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtGui import QFont
import sys
import database_manager as sqlite
import user_management
import patient_management
from __manifest__ import path_separator, load_properties, save_property
import login
import pyqtgraph as pg
from time import sleep
import patient_info
from stopwatch import Stopwatch


class Chrono(QtWidgets.QMainWindow):
    def __init__(self):
        super(Chrono, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'cronometro.ui', self) # Load the .ui file
        self.show() # Show the GUI
        
        config = load_properties()
        self.current_user = config.get('UsersSection', 'currentUser')
        
        
        self.saved_message_thread = message_thread(self.saved_msg)
        
        styles = {'color':'(162,173,194)', 'font-size':'15px'}
        self.graph.showGrid(x=True, y=True)
        self.graph.setLabel('left', 'Tiempo por vuelta', **styles)
        self.graph.setLabel('bottom', 'Días', **styles)
        self.graph.setBackground('#fdfdff')

        self.moreInfo.clicked.connect(self.show_more_info)
        self.moreInfo.hide()

        self.saveIcon.clicked.connect(self.save_times)
        self.saveIcon.hide()

        

        self.startStop.clicked.connect(self.start_crono)
        self.users.clicked.connect(self.open_users_menu)
        self.pacientesIcon.clicked.connect(self.open_patients_menu)

        self.comboPatients.setStyleSheet("QComboBox#comboPatients { border: 1px solid gray; border-radius: 5px; } QComboBox#comboPatients::down-arrow{ image: ./img/arrow.png } QComboBox#comboPatients QAbstractItemView{ background-color: #fdfdff; color: #222628; selection-background-color: #555860; selection-color: #fdfdff;}")
        self.comboPatients.setPlaceholderText("Selecciona un paciente")
        self.patients_dni = []
        self.current_patient = -1
        self.fill_combo()
        self.comboPatients.currentIndexChanged.connect(self.select_new_patient)

        self.stopwatch = Stopwatch()
        self.stopwatch.stop()
        
        self.quali_label.setStyleSheet("QWidget#quali_label{ color: black }")
        self.saved_msg.setStyleSheet("QWidget#saved_msg{ color: black }")
        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color: #fdfdff}")
        self.barraLateral.setStyleSheet("QWidget#barraLateral{ background-color: #555860; }")
        self.cronIcon.setStyleSheet("QPushButton#cronIcon::hover{ border: none; background-color: #a2adc2;} QPushButton#cronIcon::pressed{background-color: #222628;}")
        self.users.setStyleSheet("QPushButton#users::hover{ border: none; background-color: #a2adc2;} QPushButton#users::pressed{background-color: #222628;}")
        self.pacientesIcon.setStyleSheet("QPushButton#pacientesIcon::hover{ border: none; background-color: #a2adc2;} QPushButton#pacientesIcon::pressed{background-color: #222628;}")

        self.izquierda.setStyleSheet("QWidget#izquierda::hover{ border: none; background-color: #e9e8eb;} ")
        self.derecha.setStyleSheet("QWidget#derecha::hover{ border: none; background-color: #e9e8eb;} ")

        self.model = QtGui.QStandardItemModel()
        self.lapsList.setModel(self.model)
        

        self.laps_image = QtGui.QIcon('img/laps.png')
        self.restart_image = QtGui.QIcon('img/restart.png')
        self.start_image = QtGui.QIcon('img/white.png')

        self.lap_num = 0
        self.previous_time = 0
        self.lap_times = []
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.run_watch)
        self.timer.setInterval(10)
        self.mscounter = 0
        self.isreset = True
        self.showLCD()
        
        
    def show_more_info(self):
        save_property('PatientsSection', 'selectedPatient', self.current_patient)
        self.window = patient_info.Patient_info()

    def save_times(self):
        sql_con = sqlite.sqlite_connector()

        sql_con.save_lap_times(self.lap_times, self.current_patient)

        sql_con.close()
        self.saveIcon.hide()
        self.show_patient_graph()
        self.saved_message_thread.start()
    
   

    def fill_combo(self):
        sql_con = sqlite.sqlite_connector()
        patients = sql_con.get_patient_names(self.current_user)
        for user in patients:
            self.patients_dni.append(user[2])
            self.comboPatients.addItem(user[0]+" "+user[1])
        sql_con.close()

    def select_new_patient(self):


        self.current_patient = self.patients_dni[self.comboPatients.currentIndex()-1]
        self.show_patient_graph()
        self.moreInfo.show()
        
    def show_patient_graph(self):
        sql_con = sqlite.sqlite_connector()

        times = sql_con.get_patient_total_times(self.current_patient)
        dates = sql_con.get_patient_dates(self.current_patient)

        sql_con.close()
        pen = pg.mkPen(color=(162,173,194), width=4)
        self.graph.clear()
        self.graph.plot(dates, times, pen=pen, symbol='o', symbolSize=10, symbolBrush=(0,0,0))

    def record_lap(self):
        """
        Afegeix una nova lap al cronómetro
        """
        if (self.mscounter > 1000):
            this_time = float(str(self.stopwatch)[:-1])
            text = "Vuelta "+str(self.lap_num+1)+": "
            if(self.lap_num ==  0):
                text += "{:.2f}".format(this_time)
                text += " - "+get_lap_type(self.lap_num, this_time)
            else:
                text += "{:.2f}".format(this_time - self.previous_time)
                text += " - "+get_lap_type(self.lap_num, this_time - self.previous_time)
            
            
            self.lap_num += 1
            self.lap_times.append(float("{:.2f}".format(this_time - self.previous_time)))
            self.previous_time = this_time
            self.append_item_list_view(QtGui.QStandardItem(text))
            if (self.lap_num == 3):
                
                self.show_total_qualification()
                self.saveIcon.show()
                self.pause_watch()
                self.previous_time = 0
                self.append_item_list_view(QtGui.QStandardItem("VUELTAS COMPLETADAS"))
                
    def show_total_qualification(self):
        total_time = 0
        for time in self.lap_times:
            total_time += time
        self.quali_label.setText("Clasificación: "+self.get_lap_type(-1, total_time))
                
    def append_item_list_view(self, item):
        item.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.model.appendRow(item)
            
    def showLCD(self):
        """
        Aquesta funció serveix per a mostrar per pantalla el temps
        """
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
        self.saveIcon.hide()
        self.model.removeRows(0, self.model.rowCount())
        if(self.current_patient == -1):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Primero tienes que seleccionar un paciente.")
        else:
            if(self.isreset):
                self.stopwatch.start()
                self.timer.start()
                
            else:
                self.stopwatch.restart()
                self.timer.restart()

            self.startStop.setIcon(self.laps_image) # Passa a ser el botó de laps
            self.startStop.clicked.disconnect(self.start_crono) # Desconectem l'antic slot
            self.startStop.clicked.connect(self.record_lap) # Conectem el nou
            self.isreset = False
        
    def pause_watch(self):
        """
        Pausa el cronómetre quan s'aplega a 3 voltes
        """

        self.stopwatch.stop()
        self.timer.stop()
        self.startStop.setIcon(self.restart_image)
        self.startStop.clicked.disconnect(self.record_lap)
        self.startStop.clicked.connect(self.reset_watch)
    
    def reset_watch(self):
        """
        Reinicia el cronómetre
        """
        self.stopwatch.restart()
        self.mscounter = 0
        self.lap_num = 0
        self.isreset = True
        self.showLCD()
        self.lap_times = []

        self.startStop.clicked.disconnect(self.reset_watch)
        self.startStop.clicked.connect(self.start_crono)
        self.start_crono()
        

    def open_users_menu(self):
        self.new_window = user_management.Users_management()
        self.close()

    def open_patients_menu(self):
        self.new_window = patient_management.Patient_management()
        self.close()

    def closeEvent(self, event):
        self.saved_message_thread = None

class message_thread(QtCore.QThread):
    def __init__(self, qlabel):
        QtCore.QThread.__init__(self)
        self.saved_msg = qlabel

    def __del__(self):
        self.wait()

    def run(self):
        sleep(0.3)
        self.saved_msg.setText("¡Guardado!")
        sleep(2)
        self.saved_msg.setText("")

def get_lap_type(lap, time):
    config = load_properties()
    if(lap == -1): # -1 és temps total
        minTotalTime = float(config.get('TotalTimeSection', 'minimumTime'))
        maxTotalTime = float(config.get('TotalTimeSection', 'maxiumumTime'))
        if(time < minTotalTime):
            return "Leve"
        elif(time > maxTotalTime):
            return "Grave"
        else:
            return "Moderado"
    elif(lap == 0):
        minTime = float(config.get('Seg1TimeSection', 'minimumTime'))
        maxTime = float(self.config.get('Seg1TimeSection', 'maxiumumTime'))
        if(time < minTime):
            return "Leve"
        elif(time > maxTime):
            return "Grave"
        else:
            return "Moderado"
    elif(lap == 1):
        minTime = float(config.get('Seg2TimeSection', 'minimumTime'))
        maxTime = float(config.get('Seg2TimeSection', 'maxiumumTime'))
        if(time < minTime):
            return "Leve"
        elif(time > maxTime):
            return "Greu"
        else:
            return "Moderado"
    else:
        minTime = float(config.get('Seg3TimeSection', 'minimumTime'))
        maxTime = float(config.get('Seg3TimeSection', 'maxiumumTime'))
        if(time < minTime):
            return "Leve"
        elif(time > maxTime):
            return "Grave"
        else:
            return "Moderado"

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = login.Ui() # Llancem el login
    app.exec_() # Start the application