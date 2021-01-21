#!/usr/bin/python3
import sys
from os.path import dirname, realpath
sys.path.append(dirname(realpath(__file__)))
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtGui import QFont
import database_manager as sqlite
import user_management
import patient_management
from settings import Settings
from __manifest__ import path_separator, load_properties, save_property, import_db, copy_file
import login
import pyqtgraph as pg
from time import sleep
import patient_info
from stopwatch import Stopwatch



class Chrono(QtWidgets.QMainWindow):
    def __init__(self):
        super(Chrono, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi("test"+path_separator+'UI'+path_separator+'cronometro.ui', self) # Load the .ui file
        self.show() # Show the GUI
        
        config = load_properties()
        self.current_user = config.get('UsersSection', 'currentUser')
        
        self.action_import.triggered.connect(self.import_db)
        self.action_import.setShortcut(QtGui.QKeySequence("Ctrl+i"))


        self.quali_label.setVisible(False)

        self.action_export.triggered.connect(self.export_db)
        self.action_export.setShortcut(QtGui.QKeySequence("Ctrl+e"))

        self.saved_message_thread = message_thread(self.saved_msg)
        
        styles = {'color':'(162,173,194)', 'font-size':'15px'}
        self.graph.showGrid(x=True, y=True)
        self.graph.setLabel('left', 'Tiempo por vuelta', **styles)
        self.graph.setLabel('bottom', 'Días', **styles)
        self.graph.setBackground('#fdfdff')
        self.graph.setTitle("Tiempos del paciente")

        self.lapsList.setStyleSheet("QLabel#lapsList{ font-weight: bold; color: #555860; font-size: 17px; }")
        self.quali_label.setStyleSheet("QLabel#quali_label{ font-weight: bold; color: #fdfdff; font-size: 15px; background-color: #222628; border: 2px solid #909293; }")

        self.moreInfo.setStyleSheet("QPushButton#moreInfo{ border: 2px solid #717987; font-weight: bold; color: white; background-color: #a2adc2; } QPushButton#moreInfo::hover{ background-color: #BDC5D4;} QPushButton#moreInfo::pressed{background-color: #717987;}")
        self.moreInfo.clicked.connect(self.show_more_info)
        self.moreInfo.hide()

        self.saveIcon.clicked.connect(self.save_times)
        self.saveIcon.hide()

        self.saveIcon.setStyleSheet("QPushButton#saveIcon{ border-radius: 20px; font-weight: bold; color: white; background-color: #a2adc2; } QPushButton#saveIcon::hover{ background-color: #BDC5D4;} QPushButton#saveIcon::pressed{background-color: #717987;}")
        self.startStop.setStyleSheet("QPushButton#startStop{ border-radius: 20px; font-weight: bold; color: white; background-color: #a2adc2; } QPushButton#startStop::hover{ background-color: #BDC5D4;} QPushButton#startStop::pressed{background-color: #717987;}")
        self.startStop.clicked.connect(self.start_crono)
        self.users.clicked.connect(self.open_users_menu)
        self.pacientesIcon.clicked.connect(self.open_patients_menu)
        self.settingsIcon.clicked.connect(self.open_settings)

        self.comboPatients.setStyleSheet("QComboBox#comboPatients QAbstractItemView{ background-color: #fdfdff; color: #222628; selection-background-color: #555860; selection-color: #fdfdff;}")
        self.comboPatients.setPlaceholderText("Selecciona un paciente")
        self.patients_dni = []
        self.current_patient = -1
        self.fill_combo()
        self.comboPatients.currentIndexChanged.connect(self.select_new_patient)

        self.stopwatch = Stopwatch()
        self.stopwatch.stop()
        
        self.saved_msg.setStyleSheet("QWidget#saved_msg{ color: black }")
        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color: #fdfdff}")
        self.barraLateral.setStyleSheet("QWidget#barraLateral{ background-color: #555860; }")
        self.cronIcon.setStyleSheet("QPushButton#cronIcon::hover{ border: none; background-color: #a2adc2;} QPushButton#cronIcon::pressed{background-color: #222628;}")
        self.users.setStyleSheet("QPushButton#users::hover{ border: none; background-color: #a2adc2;} QPushButton#users::pressed{background-color: #222628;}")
        self.pacientesIcon.setStyleSheet("QPushButton#pacientesIcon::hover{ border: none; background-color: #a2adc2;} QPushButton#pacientesIcon::pressed{background-color: #222628;}")
        self.settingsIcon.setStyleSheet("QPushButton#settingsIcon::hover{ border: none; background-color: #a2adc2;} QPushButton#settingsIcon::pressed{background-color: #222628;}")

        self.izquierda.setStyleSheet("QWidget#izquierda::hover{ border: none; background-color: #e9e8eb;} ")
        self.derecha.setStyleSheet("QWidget#derecha::hover{ border: none; background-color: #e9e8eb;} ")

        self.laps_image = QtGui.QIcon('test/img/laps.png')
        self.restart_image = QtGui.QIcon('test/img/restart.png')
        self.start_image = QtGui.QIcon('test/img/white.png')

        self.text = ""
        self.lap_num = 0
        self.previous_time = 0
        self.lap_times = []
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.run_watch)
        self.timer.setInterval(10)
        self.mscounter = 0
        self.isreset = True
        self.showLCD()

    def open_settings(self):
        """ 
        Obri la finestra dels settings on es canviaràn els temps màxims i mínims del segments i total.
        """
        self.new_window = Settings()

    def export_db(self):
        """
        Exportar la BD actual
        """
        export_path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', QtCore.QDir.homePath(), "Archivo SQLite (*.db)") # Arrepleguem el nou path
        
        copy_file(load_properties().get('DatabaseSection', 'dbname'), export_path[0]) # Copiem la BD de la seva path a la path donada per l'usuari
        QtWidgets.QMessageBox.information(self, 'Parkthon', "La base de datos ha sido exportada con éxito") # Mostrem un missatge d'éxit

    def import_db(self):
        """
        Importar una nova BD. Com que aquesta funció també és utilitzada en login.py, s'ha implementat en l'arxiu __manifest__.py
        """
        import_db(self)

    def show_more_info(self):
        """
        Mostrem més informació del pacient actual
        """
        self.window = patient_info.Patient_info(self.current_user, self.current_patient) # Llancem la nova finestra

    def save_times(self):
        """
        Aquesta funció crida al controlador de la DB per guardar una llista de temps al pacient actual
        """
        sql_con = sqlite.sqlite_connector() # Creem la connexió

        sql_con.save_lap_times(self.lap_times, self.current_patient, self.observations.toPlainText()) # Guardem els temps en l'usuari actual

        sql_con.close() # Tanquem la connexió
        self.saveIcon.hide() # Amaguem l'icona de guardar ja que ja s'ha guardat
        self.show_patient_graph() # Afegim aquest ultim temps a la gràfica
        self.saved_message_thread.start() # Escomencem el thread que mostrarà que el temps ha sigut guardat
    
   

    def fill_combo(self):
        """
        Funció que plena el QComboBox amb tots els pacients del metge actual
        """
        sql_con = sqlite.sqlite_connector() # Arrepleguem la connexió a SQLite
        patients = sql_con.get_patient_names(self.current_user) # Arrepleguem una matriu amb les dades de tots els pacients del metge actual
        sql_con.close() # Tanquem la connexió una vegada recuperades les dades
        for patient in patients:
            self.patients_dni.append(patient[2]) # Ens guardem els DNI de tots els pacients de forma interna
            self.comboPatients.addItem(patient[0]+" "+patient[1]) # Afegim el nom i cognom al QComboBox
        
    def select_new_patient(self):
        """
        Seleccionem el nou pacient, en el que es realitzarán totes les accions com registrar nous temps, mostrar la gràfica, etc.
        """
        self.current_patient = self.patients_dni[self.comboPatients.currentIndex()] # Guardem de forma interna el DNI del pacient depenent del index del QComboBox (Per això guardavem els DNI en una llista, la cual està de forma paral.lela)
        self.show_patient_graph() # Carreguem la gràfica del pacient
        self.moreInfo.show() # Mostrem el botó de més informació sobre el pacient
        
    def show_patient_graph(self):
        """
        Mostra/Carrega la gràfica del pacient
        """
        
        
        sql_con = sqlite.sqlite_connector() # Arrepleguem el connector a la BD

        total_times = sql_con.get_patient_total_times(self.current_patient) # Arrepleguem en forma de llista tots els temps dels pacients
        seg1_times = sql_con.get_patient_segment_times(self.current_patient, "lap1")
        seg2_times = sql_con.get_patient_segment_times(self.current_patient, "lap2")
        seg3_times = sql_con.get_patient_segment_times(self.current_patient, "lap3")
        dates = sql_con.get_patient_dates(self.current_patient) # Arrepleguem els díes en els que es van realitzar les proves (Son llistes paral.leles)

        sql_con.close() # Tanquem la connexió
        self.graph.clear() # Esborrem tot el que hi ha en el gràfic
        self.graph.addLegend() # Inicialitzem la llegenda
        self.graph.plot(dates, total_times, name="Total", pen=pg.mkPen(color=(162,173,194), width=4), symbol='o', symbolSize=10, symbolBrush=(0,0,0)) # Mostrem les dades
        self.graph.plot(dates, seg1_times, name="Segmento 1", pen=pg.mkPen(color=(255,0,0), width=4), symbol='o', symbolSize=5, symbolBrush=(0,0,0))
        self.graph.plot(dates, seg2_times, name="Segmento 2", pen=pg.mkPen(color=(255,255,0), width=4), symbol='o', symbolSize=5, symbolBrush=(0,0,0))
        self.graph.plot(dates, seg3_times, name="Segmento 3", pen=pg.mkPen(color=(255,0,255), width=4), symbol='o', symbolSize=5, symbolBrush=(0,0,0))
    def record_lap(self):
        """
        Afegeix una nova lap al cronómetro
        """
        if (self.mscounter > 1000): # El contador ha de ser major a un segon per evitar problemes de compilació
            this_time = float(str(self.stopwatch)[:-1]) # Arrepleguem com a float el temps de la lap actual
            self.text += "Vuelta "+str(self.lap_num+1)+": " # Comencem a crear el text que es mostrarà en el número de volta
            if(self.lap_num ==  0): # Si és la primera volta
                self.text += "{:.2f}".format(this_time) # Al text li afegim el temps formatejat amb sols 2 decimals
                lap_type = get_lap_type(self.lap_num, this_time) # Arrepleguem el tipus de lap (Lleu, Moderat, Greu)
                color = get_color_type(lap_type) # Arrepleguem el color (Depenent de la lap)
            else:
                lap_type = get_lap_type(self.lap_num, this_time - self.previous_time)
                color = get_color_type(lap_type)
                self.text += "{:.2f}".format(this_time - self.previous_time)

            self.text += " - <span style='color:"+color+";'>"+lap_type+"</span><br/>"
            self.lapsList.setText(self.text)
            
            self.lap_num += 1
            self.lap_times.append(float("{:.2f}".format(this_time - self.previous_time)))
            self.previous_time = this_time
            if (self.lap_num == 3):
                
                self.show_total_qualification()
                self.saveIcon.show()
                self.pause_watch()
                self.previous_time = 0
                self.text += "<span style='color: #222628;'>¡VUELTAS COMPLETADAS!</span>"
                self.lapsList.setText(self.text)
                
            
                
    def show_total_qualification(self):
        self.quali_label.setVisible(True)
        total_time = 0
        for time in self.lap_times:
            total_time += time
        lap_type = get_lap_type(-1, total_time)
        color = get_color_type(lap_type)
        
        self.quali_label.setText("Clasificación: <span style='color:"+color+";'>"+lap_type+"</span>")
            
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
        self.lapsList.setText("")
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
        self.text = ""
        self.quali_label.setText("")
        self.quali_label.setVisible(False)

        self.startStop.clicked.disconnect(self.reset_watch)
        self.startStop.clicked.connect(self.start_crono)
        self.start_crono()
        

    def open_users_menu(self):
        self.new_window = user_management.Users_management()
        self.close()

    def open_patients_menu(self):
        self.new_window = patient_management.Patient_management()
        self.close()


class message_thread(QtCore.QThread):
    def __init__(self, qlabel):
        QtCore.QThread.__init__(self)
        self.saved_msg = qlabel

    def __del__(self):
        try:
            self.wait()
        except RuntimeError:
            pass

    def run(self):
        sleep(0.3)
        self.saved_msg.setText("¡Guardado!")
        sleep(2)
        self.saved_msg.setText("")

def get_lap_type(lap, time, seg_id=-1):
    sql_con = sqlite.sqlite_connector()

    if(lap == -1): # -1 és temps total
        minTotalTime = sql_con.get_segment_time("total_min_time", seg_id)
        maxTotalTime = sql_con.get_segment_time("total_max_time", seg_id)
        if(time < minTotalTime):
            return "Leve"
        elif(time > maxTotalTime):
            return "Grave"
        else:
            return "Moderado"
    elif(lap == 0):
        minTime = sql_con.get_segment_time("seg1_min_time", seg_id)
        maxTime = sql_con.get_segment_time("seg1_max_time", seg_id)
        if(time < minTime):
            return "Leve"
        elif(time > maxTime):
            return "Grave"
        else:
            return "Moderado"
    elif(lap == 1):
        minTime = sql_con.get_segment_time("seg2_min_time", seg_id)
        maxTime = sql_con.get_segment_time("seg2_max_time", seg_id)
        if(time < minTime):
            return "Leve"
        elif(time > maxTime):
            return "Grave"
        else:
            return "Moderado"
    else:
        minTime = sql_con.get_segment_time("seg3_min_time", seg_id)
        maxTime = sql_con.get_segment_time("seg3_max_time", seg_id)
        if(time < minTime):
            return "Leve"
        elif(time > maxTime):
            return "Grave"
        else:
            return "Moderado"

def get_color_type(lap_type):
    if(lap_type == "Leve"):
        return "#006400"
    elif(lap_type == "Moderado"):
        return "#e4d96f"
    else:
        return "#8b0000"

def main():
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = login.Ui() # Llancem el login
    app.exec_() # Start the application

if __name__ == "__main__":
    main()