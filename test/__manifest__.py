from os.path import dirname, join, isfile
import configparser
import database_manager as sqlite
from PyQt5 import QtWidgets, QtCore, uic
import shutil

CONFIG_FILE_PATH = join(dirname(__file__), ".ConfigFile.properties")

def create_properties():
    """
    Crea l'arxiu de propietats en cas de que no existisca
    """
    if(not file_exists(CONFIG_FILE_PATH)): # Si estem on està el chrono i no existeix el config file
        config = configparser.RawConfigParser()
        config.add_section('DatabaseSection')
        
        config.set('DatabaseSection', 'dbname', join(dirname(__file__), "DB/parkthon.db"))
        config.add_section("UsersSection")
        config.set('UsersSection', 'currentUser', '')
        config.add_section("ShowCloseMessage")
        config.set('ShowCloseMessage', 'ShowCloseMessage', 'True')

        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)

def load_properties():
    """
    Carrega l'arxiu de propietats

    Eixida:

        (Object) L'apuntador al fitxer de configuraicó
    """
    config = configparser.RawConfigParser()
    config.read(CONFIG_FILE_PATH)
    return config

def save_property(section, key, value):
    """
    Guarda una propietat donada la clau i la secció en el fitxer de configuració.

    Entrada:

        section (String) La secció

        key (String) La clau

        value (String) El valor
    """
    config = load_properties()
    config.set(section, key, value)     
    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)

def file_exists(file):
    """ 
    Comprova si el fitxer enviat com a paràmetre existeix o no

    Entrada:

        file (String) La ruta del fitxer

    Eixida:

        (Boolean) Si existeix o no
    """
    return isfile(file)

def copy_file(file_path, new_path):
    """
    Copia el fitxer enviat com a paràmetre a la ruta enviada com a segón parámetre

    Entrada:

        1. (String) Ruta del fitxer

        2. (String) La nova path del fitxer
    """
    shutil.copyfile(file_path, new_path)

def import_db(window):
    """
    Obri un QFileDialog per a importar una nova *.db

    Entrada:
        
        (QMainWindow) La finestra on s'executarà el QFileDialog
    """
    new_db_path = QtWidgets.QFileDialog.getOpenFileName(window, "Open file", QtCore.QDir.homePath(), "Archivo SQLite (*.db)")
    if (new_db_path[0] != ""):
        config = load_properties()
        save_property('DatabaseSection', 'dbname', new_db_path[0])
    
def comprobation_message(title, msg, by="Sí", bn="No"):
    box = QtWidgets.QMessageBox()
    box.setIcon(QtWidgets.QMessageBox.Question)
    box.setWindowTitle(title)
    box.setText(msg)
    box.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
    buttonY = box.button(QtWidgets.QMessageBox.Yes)
    buttonY.setText(by)
    buttonN = box.button(QtWidgets.QMessageBox.No)
    buttonN.setText(bn)
    box.exec_()
    return box.clickedButton() == buttonY

def calculate_imc(weight, height):
    if(weight != "" and height != ""):
        try:
            height = float(height)
            if(height > 50):
                height /= 100
            return str(float(weight) / (height * height))
        except ValueError:
            pass

def photo_to_blob(pixmap):
    ba = QtCore.QByteArray()
    buff = QtCore.QBuffer(ba)
    buff.open(QtCore.QIODevice.WriteOnly) 
    pixmap.save(buff, "PNG")
    return ba.data()

def load_doctors(combobox, doctor):
    sql_con = sqlite.sqlite_connector()
    doctors = sql_con.get_users()
    sql_con.close()
    for i in range(0, len(doctors)):
        combobox.addItem(doctors[i][0])
        if(doctor == doctors[i][0]):
            combobox.setCurrentIndex(i)
    return combobox

def check_dni(text_edit, palabra='TRWAGMYFPDXBNJZSQVHLCKE'):
        nif = text_edit.text()

        try:
            if (len(nif) == 9):
                dni = ""
                for i in range(0, 8):
                    dni += nif[i]
                
                letra = palabra[int(dni) % 23]
                if(nif[8] == letra):
                    text_edit.setStyleSheet("background-color: green;")
                else:
                    text_edit.setStyleSheet("background-color: red;")
        except ValueError:
            text_edit.setStyleSheet("background-color: red;")
            

def salir():
    if(load_properties().get('ShowCloseMessage', 'ShowCloseMessage') == 'True'):
        return Comprobacion_salida().exec()
    return True

class Comprobacion_salida(QtWidgets.QDialog):
    def __init__(self):
        super(Comprobacion_salida, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(join(dirname(__file__), "UI/comprobacion_salida.ui"), self) # Load the .ui file
            
        self.finished.connect(self.check_checkbox)

    def check_checkbox(self):
        if(self.checkBox.isChecked()):
            save_property('ShowCloseMessage', 'ShowCloseMessage', 'False')

    