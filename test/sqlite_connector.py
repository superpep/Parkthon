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

        cursorObj = self.__con.cursor()
        cursorObj.execute("SELECT * FROM users where DNI = '"+dni+"'")

        rows = cursorObj.fetchall()

        if(encrypt.check_encrypted_password(raw_passwd, rows[0][1])): # Comparem la contrasenya sense encriptar amb l'encriptada
            print("LOGIN CORRECT")
        else:
            print("LOGIN INCORRECT")

    def create_user(self, dni, raw_passwd):
        entities = (dni, encrypt.encrypt_password(raw_passwd)) # Encriptem la contrasenya

        cursorObj = self.__con.cursor()
        cursorObj.execute("INSERT INTO users VALUES(?, ?)", entities)
        self.__con.commit()

    def create_initial_table(self):
        cursorObj = self.__con.cursor()
        cursorObj.execute("CREATE TABLE users(DNI varchar(9) PRIMARY KEY, passwd password)")
        self.__con.commit()  

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

