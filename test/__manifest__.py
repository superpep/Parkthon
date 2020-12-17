import os
import configparser
from PyQt5 import QtWidgets, QtCore
import shutil

path_separator = os.path.sep
CONFIG_FILE_NAME = "ConfigFile.properties"

def create_properties():
    """
    Crea l'arxiu de propietats en cas de que no existisca
    """
    if(file_exists("chrono.py") and not file_exists(CONFIG_FILE_NAME)): # Si estem on està el chrono i no existeix el config file
        config = configparser.RawConfigParser()
        config.add_section('DatabaseSection')
        
        config.set('DatabaseSection', 'dbname', 'DB'+path_separator+'parkthon.db')
        config.add_section("UsersSection")
        config.set('UsersSection', 'currentUser', '')
        config.add_section("PatientsSection")
        config.set('PatientsSection', 'selectedPatient', '')


        config.add_section("TotalTimeSection")
        config.set('TotalTimeSection', 'minimumTime', 41.91)
        config.set('TotalTimeSection', 'maxiumumTime', 60.32)
        
        config.add_section("Seg1TimeSection")
        config.set('Seg1TimeSection', 'minimumTime', 17.16)
        config.set('Seg1TimeSection', 'maxiumumTime', 23.56)

        config.add_section("Seg2TimeSection")
        config.set('Seg2TimeSection', 'minimumTime', 15.14)
        config.set('Seg2TimeSection', 'maxiumumTime', 25.90)

        config.add_section("Seg3TimeSection")
        config.set('Seg3TimeSection', 'minimumTime', 10.43)
        config.set('Seg3TimeSection', 'maxiumumTime', 13.34)
        with open(CONFIG_FILE_NAME, 'w') as configfile:
            config.write(configfile)

def load_properties():
    """
    Carrega l'arxiu de propietats

    Eixida:

        (Object) L'apuntador al fitxer de configuraicó
    """
    config = configparser.RawConfigParser()
    config.read(CONFIG_FILE_NAME)
    return config

def save_property(section, key, value):
    """
    Guarda una propietat donada la clau i la secció en el fitxer de configuració.

    Entrada:

        section (String) La secció

        key (String) La clau

        value (String) El valor\
    """
    config = load_properties()
    config.set(section, key, value)     
    with open(CONFIG_FILE_NAME, 'w') as configfile:
        config.write(configfile)

def file_exists(file):
    """ 
    Comprova si el fitxer enviat com a paràmetre existeix o no

    Entrada:

        file (String) La ruta del fitxer

    Eixida:

        (Boolean) Si existeix o no
    """
    return os.path.isfile(file)

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