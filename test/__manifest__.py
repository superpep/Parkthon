import os
import configparser

path_separator = os.path.sep
CONFIG_FILE_NAME = "ConfigFile.properties"

def create_properties():
    if(not file_exists(".gitignore")):
        config = configparser.RawConfigParser()
        config.add_section('DatabaseSection')
        config.set('DatabaseSection', 'dbname', 'parkthon.db')
        config.add_section("UsersSection")
        config.set('UsersSection', 'currentUser', '')
        with open(CONFIG_FILE_NAME, 'w') as configfile:
            config.write(configfile)

def load_properties():
    config = configparser.RawConfigParser()
    config.read(CONFIG_FILE_NAME)
    return config

def file_exists(file):
    return os.path.isfile(file)
