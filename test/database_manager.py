import sqlite3
import os.path
import encrypt
from login import getOsSeparator

DB = "DB"+getOsSeparator()+"parkthon.db"

class sqlite_connector:
    def __init__(self):
        try:
            self.__con = sqlite3.connect(DB)
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

    def create_user(self, dni, raw_passwd, isAdmin):
        """
        Crea l'usuari amb les dades enviades

        Entrada:
            dni (string): Dni de l'usuari
            raw_passwd (string): Contrasenya sense encriptar de l'usuari
        """
        entities = (dni, encrypt.encrypt_password(raw_passwd), isAdmin) # Encriptem la contrasenya

        cursorObj = self.__con.cursor()
        cursorObj.execute("INSERT INTO users VALUES(?, ?, ?)", entities)
        self.__con.commit()

    def create_initial_table(self):
        """
        Crea la primera taula quan es crea la base de dades
        """
        cursorObj = self.__con.cursor()
        cursorObj.execute("CREATE TABLE users(DNI varchar(9) PRIMARY KEY, passwd password, isAdmin BOOLEAN)")
        self.__con.commit()  

    def get_users(self):
        cursorObj = self.__con.cursor()
        cursorObj.execute("SELECT DNI FROM users")

        rows = cursorObj.fetchall()
        return rows

    def delete_user(self, dni):
        """
        Elimina l'usuari en cas de que no siga administrador l'unic admin que queda

        Entrada:
            dni (string): Dni de l'usuari
        Eixida:
            (boolean): Si l'usuari s'ha eliminat o no
        """
        if(self.check_admins(dni)):
            return False

        cursorObj = self.__con.cursor()
        cursorObj.execute("DELETE FROM users WHERE DNI = '"+dni+"'")
        self.__con.commit()
        return True
    
    def check_admins(self, dni):
        """
        Comprova cuants admins hi han i en cas de ser sols 1, comprova que si és o no el que s'ha passat com a parámetre

        Entrada:
            dni (string): Dni de l'usuari
        Eixida:
            (boolean): Si es pot seguir amb el delete (Més d'un admin o l'usuari no és admin) o si no es pot (Sols queda 1 admin i és l'usuari)
        """
        cursorObj = self.__con.cursor()
        cursorObj.execute("SELECT count(*) FROM users where isAdmin = 1") # MIRA A VEURE QUANS ADMINS HI HAN
        rows = cursorObj.fetchall()
        if(rows[0][0] == 1):
            cursorObj.execute("SELECT isAdmin FROM users where DNI = '"+dni+"'") # EN CAS DE SOLS UN ADMIN, COMPROVA QUE NO ÉS EL QUE ES VOL ESBORRAR
            rows = cursorObj.fetchall()
            return (rows[0][0] == 1) # RETORNA SI L'USUARI ÉS ADMIN O NO
        return False

def database_exists():
    """
    Funció que comprova si la base de dades existeix o no

    Eixida:
        (boolean) Si existeix o no
    """
    return os.path.isfile(DB)
