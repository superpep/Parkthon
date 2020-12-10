import sqlite3
import encrypt
from __manifest__ import path_separator, file_exists, load_properties

class sqlite_connector:
    def __init__(self):
        config = load_properties()
        self.DB = "DB"+path_separator+config.get('DatabaseSection', 'dbname')
        if(self.database_exists()):
            try:
                self.__con = sqlite3.connect(self.DB)
            except sqlite3.Error:
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
            isAdmin (boolean): Si és admin o no
        """

        cursorObj = self.__con.cursor()
        cursorObj.execute("INSERT INTO users VALUES(?, ?, ?)", (dni, encrypt.encrypt_password(raw_passwd), isAdmin))
        self.__con.commit()

    def create_initial_table(self):
        """
        Crea la primera taula quan es crea la base de dades
        """
        cursorObj = self.__con.cursor()
        cursorObj.execute("CREATE TABLE users(DNI varchar(9) PRIMARY KEY, passwd password, isAdmin BOOLEAN)")
        cursorObj.execute("CREATE TABLE patients(DNI varchar(9) primary key, name varchar(20), surname varchar(20), doctor varchar(9), CONSTRAINT fk_doctor FOREIGN KEY(doctor) REFERENCES users(dni))")
        cursroObj.execute("CREATE TABLE times(patient varchar(9), day date, lap1 float, lap2 float, lap3 float, CONSTRAINT pk PRIMARY KEY(patient, day) CONSTRAINT fk_pacient FOREIGN KEY(patient) REFERENCES patients(dni));")
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

        self.delete_dni_from_table(dni, "users")
        return True
    
    def delete_patient(self, dni):
        self.delete_dni_from_table(dni, "patients")

    def delete_dni_from_table(self, dni, table):
        cursorObj = self.__con.cursor()
        cursorObj.execute("DELETE FROM "+table+" WHERE DNI = '"+dni+"'")
        self.__con.commit()

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
            return self.is_admin(dni) # EN CAS DE SOLS UN ADMIN, COMPROVA QUE NO ÉS EL QUE ES VOL ESBORRAR
        return False

    def change_password(self, dni, raw_passwd):
        """
        Canvia la contrasenya de l'usuari amb dni passat com a paràmetre

        Entrada:
            dni (string): Dni de l'usuari al que es canvia la contrasenya
            raw_passwd (string): Contrasenya sense encriptar per la que es canviarà
        """
        enc_pass = encrypt.encrypt_password(raw_passwd)
        cursorObj = self.__con.cursor()
        cursorObj.execute("UPDATE users SET passwd = '"+enc_pass+"' WHERE DNI = '"+dni+"'")
        self.__con.commit()

    def is_admin(self, dni):
        """
        Comprova si el DNI passat és o no administrador

        Entrada:
            dni (string): Dni de l'usuari
        Eixida:
            (boolean): Si és o no
        """
        cursorObj = self.__con.cursor()
        cursorObj.execute("SELECT isAdmin FROM users where DNI = '"+dni+"'")
        rows = cursorObj.fetchall()
        return (rows[0][0] == 1) # RETORNA SI L'USUARI ÉS ADMIN O NO

    def get_patient_names(self, doctor_dni):
        """
        Retorna els pacients asociats al metge passat com a paràmetre

        Entrada:
            doctor_dni (string): Dni del metge
        
        Eixida:
            (patients): Matriu de pacients
        """
        cursorObj = self.__con.cursor()
        cursorObj.execute("SELECT name, surname, dni FROM patients where doctor = '"+doctor_dni+"'")
        return cursorObj.fetchall()

    def addPatient(self, dni, name, surname, doctor):
        cursorObj = self.__con.cursor()
        cursorObj.execute("INSERT INTO patients VALUES (?, ?, ?, ?)", (dni, name, surname, doctor))
        self.__con.commit()
    
    def save_lap_times(self, lap_times, patient):
        cursorObj = self.__con.cursor()
        cursorObj.execute("INSERT INTO times VALUES(?, datetime('now'), ?, ?, ?)", (patient, lap_times[0], lap_times[1], lap_times[2]))
        self.__con.commit()

    def get_patient_total_times(self, patient):
        cursorObj = self.__con.cursor()
        rows = cursorObj.execute("SELECT lap1, lap2, lap3 from times where patient = '"+patient+"'")
        total_lap_times = []
        for row in rows:
            total_lap_times.append(round(row[0]+row[1]+row[2], 2))
        return total_lap_times

    def get_patient_dates(self, patient):
        cursorObj = self.__con.cursor()
        rows = cursorObj.execute("SELECT day from times where patient = '"+patient+"'")
        days = []
        count = 0
        for row in rows:
            days.append(count)
            count += 1
        return days

    def close(self):
        self.__con.close

    def database_exists(self):
        """
        Funció que comprova si el fitxer existeix o no

        Eixida:
            (boolean) Si existeix o no
        """
        return file_exists(self.DB)

