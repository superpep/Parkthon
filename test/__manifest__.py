import os
import configparser

path_separator = os.path.sep
CONFIG_FILE_NAME = "ConfigFile.properties"

def create_properties():
    if(file_exists("chrono.py") and not file_exists(CONFIG_FILE_NAME)): # Si estem on està el chrono i no existeix el config file
        config = configparser.RawConfigParser()
        config.add_section('DatabaseSection')
        config.set('DatabaseSection', 'dbname', 'parkthon.db')
        config.add_section("UsersSection")
        config.set('UsersSection', 'currentUser', '')
        config.add_section("PatientsSection")
        config.set('PatientsSection', 'selectedPatient', '')
        with open(CONFIG_FILE_NAME, 'w') as configfile:
            config.write(configfile)

def load_properties():
    config = configparser.RawConfigParser()
    config.read(CONFIG_FILE_NAME)
    return config

def save_property(section, key, value):
    config = load_properties()
    config.set(section, key, value)     
    with open(CONFIG_FILE_NAME, 'w') as configfile:
        config.write(configfile)

def file_exists(file):
    return os.path.isfile(file)
