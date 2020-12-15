from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import database_manager as sqlite
import user_management
import patient_management
from __manifest__ import CONFIG_FILE_PATH, load_properties
import login
import pyqtgraph as pg
from stopwatch import Stopwatch


class Chrono(QtWidgets.QMainWindow):
    def __init__(self):
        super(Chrono, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'cronometro.ui', self) # Load the .ui file
        self.show() # Show the GUI
        
        config = load_properties()
        self.current_user = config.get('UsersSection', 'currentUser')
        
        styles = {'color':'(53,100,184)', 'font-size':'15px'}
        self.graph.showGrid(x=True, y=True)
        self.graph.setLabel('left', 'Tiempo por vuelta', **styles)
        self.graph.setLabel('bottom', 'Días', **styles)
        self.graph.setBackground('#f0f0f0')


        self.startStop.clicked.connect(self.start_crono)
        self.users.clicked.connect(self.open_users_menu)
        self.pacientesIcon.clicked.connect(self.open_patients_menu)

        self.comboPatients.addItem("Selecciona un paciente")
        self.patients_dni = []
        self.current_patient = -1
        self.fill_combo()
        self.comboPatients.currentIndexChanged.connect(self.select_new_patient)

        self.edit_welcome()

        self.stopwatch = Stopwatch()
        self.stopwatch.stop()
        
        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color: #f0f0f0}")
        self.barraLateral.setStyleSheet("QWidget#barraLateral{ background-color: #d6d6d6; }")
        self.cronIcon.setStyleSheet("QPushButton#cronIcon::hover{ border: none; background-color: #EEEEEE;} QPushButton#cronIcon::pressed{background-color: #555555;}")
        self.users.setStyleSheet("QPushButton#users::hover{ border: none; background-color: #EEEEEE;} QPushButton#users::pressed{background-color: #555555;}")
        self.pacientesIcon.setStyleSheet("QPushButton#pacientesIcon::hover{ border: none; background-color: #EEEEEE;} QPushButton#pacientesIcon::pressed{background-color: #555555;}")

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
        
    def show_patient_graph(self):
        sql_con = sqlite.sqlite_connector()

        times = sql_con.get_patient_total_times(self.current_patient)
        dates = sql_con.get_patient_dates(self.current_patient)

        sql_con.close()
        pen = pg.mkPen(color=(53,100,184), width=4)
        self.graph.clear()
        self.graph.plot(dates, times, pen=pen, symbol='o', symbolSize=10, symbolBrush=(0,0,0))

    def edit_welcome(self):
        self.bienvenida.setText("Bienvenido/a, "+self.current_user+"." )

    def record_lap(self):
        """
        Afegeix una nova lap al cronómetro
        """
        if (self.mscounter > 1000):
            this_time = float(str(self.stopwatch)[:-1])
            text = "Vuelta "+str(self.lap_num+1)+": "
            if(self.lap_num ==  0):
                text += "{:.2f}".format(this_time)
            else:
                text += "{:.2f}".format(this_time - self.previous_time)
            
            self.lap_num += 1
            self.lap_times.append(float("{:.2f}".format(this_time - self.previous_time)))
            self.previous_time = this_time
            self.append_item_list_view(QtGui.QStandardItem(text))
            if (self.lap_num == 3):
                sql_con = sqlite.sqlite_connector()

                sql_con.save_lap_times(self.lap_times, self.current_patient)

                sql_con.close()
                self.pause_watch()
                self.previous_time = 0
                self.append_item_list_view(QtGui.QStandardItem("VUELTAS COMPLETADAS"))
                self.show_patient_graph()
                
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
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = login.Ui() # Llancem el login
    app.exec_() # Start the application