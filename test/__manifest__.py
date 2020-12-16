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
