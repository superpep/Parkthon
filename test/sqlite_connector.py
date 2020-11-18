import sqlite3
import os.path
import encrypt



class sqlite_connector:
    def __init__(self, db_name):
        try:
            self.__con = sqlite3.connect(db_name)
        except Error:
            print(sqlite3.Error)

    def login(self, dni, raw_passwd):
        """
        Comprova si el login és correcte o no

        Entrada:
            dni (string): Dni de l'usuari
            raw_passwd (string): Contrasenya sense encriptar de l'usuari

        Eixida:
            (boolean) Si el login és correcte o no
        """
        cursorObj = self.__con.cursor()
        cursorObj.execute("SELECT * FROM users where DNI = '"+dni+"'")

        rows = cursorObj.fetchall()

        for row in rows: 
            return encrypt.check_encrypted_password(raw_passwd, row[1])
        return False # Si ve per aci significa que rows no té ninguna columna per a mostrar, el que significa que el DNI NO és correcte

    def create_user(self, dni, raw_passwd):
        """
        Crea l'usuari amb les dades enviades

        Entrada:
            dni (string): Dni de l'usuari
            raw_passwd (string): Contrasenya sense encriptar de l'usuari
        """
        entities = (dni, encrypt.encrypt_password(raw_passwd)) # Encriptem la contrasenya

        cursorObj = self.__con.cursor()
        cursorObj.execute("INSERT INTO users VALUES(?, ?)", entities)
        self.__con.commit()

    def create_initial_table(self):
        """
        Crea la primera taula quan es crea la base de dades
        """
        cursorObj = self.__con.cursor()
        cursorObj.execute("CREATE TABLE users(DNI varchar(9) PRIMARY KEY, passwd password)")
        self.__con.commit()  

    def get_users(self):
        cursorObj = self.__con.cursor()
        cursorObj.execute("SELECT DNI FROM users")

        rows = cursorObj.fetchall()
        return rows

def database_exists(db_name):
    """
    Funció que comprova si la base de dades existeix o no

    Entrada:
        db_name (string): Nom de la base de dades

    Eixida:
        (boolean) Si existeix o no
    """
    if os.path.isfile(db_name):
        return True
    else:
        return False

