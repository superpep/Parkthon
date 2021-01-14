import sqlite3
import encrypt
from chrono import get_lap_type
from os import mkdir, path
from __manifest__ import path_separator, file_exists, load_properties

class sqlite_connector:
    def __init__(self):
        config = load_properties()
        if(not path.isdir("DB")):
            mkdir("DB")
        self.DB = config.get('DatabaseSection', 'dbname')
        self.__con = None
        if(self.database_exists()):
            try:
                self.__con = sqlite3.connect(self.DB)
            except sqlite3.Error:
                print(sqlite3.Error)
    def get_con(self):
        return self.__con
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
        cursorObj.execute("SELECT dni, passwd FROM users where DNI = '"+dni+"' and isActive = 1")

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
        cursorObj.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (dni, encrypt.encrypt_password(raw_passwd), isAdmin, True))
        self.__con.commit()

    def create_initial_table(self):
        """
        Crea la primera taula quan es crea la base de dades
        """
        self.__con = sqlite3.connect(self.DB) # Aço crea la BD
        cursorObj = self.__con.cursor()
        cursorObj.execute("CREATE TABLE users(DNI varchar(9) PRIMARY KEY, passwd password, isAdmin BOOLEAN, isActive BOOLEAN)")
        cursorObj.execute("""CREATE TABLE patients(
            DNI varchar(9) primary key, 
            name varchar(20), 
            surname varchar(20), 
            doctor varchar(9), 
            address varchar(20), 
            tel INTEGER, 
            mail varchar(30), 
            SIP INTEGER, 
            height FLOAT, 
            weight FLOAT, 
            birth_date DATE, 
            gender CHAR, 
            diag_date DATE, 
            illness_fase INTEGER, 
            imc FLOAT, 
            body_fat FLOAT,
            medication varchar(100), 
            face_photo BLOB,
            body_photo BLOB,
            CONSTRAINT fk_doctor 
                FOREIGN KEY(doctor) 
                REFERENCES users(dni)
            )""")
        cursorObj.execute("""CREATE TABLE times(
            patient varchar(9) NOT NULL,
            day date NOT NULL, 
            lap1 float, 
            lap2 float, 
            lap3 float, 
            reference_times INTEGER,
            CONSTRAINT pk 
                PRIMARY KEY(patient, day), 
            CONSTRAINT fk_pacient 
                FOREIGN KEY(patient) 
                REFERENCES patients(dni),
            CONSTRAINT fk_reference_times 
                FOREIGN KEY(reference_times) 
                REFERENCES segment_times(ID)
            )""")
        cursorObj.execute("CREATE TABLE segment_times(ID INTEGER PRIMARY KEY AUTOINCREMENT, total_min_time float, total_max_time float, seg1_min_time float, seg1_max_time float, seg2_min_time float, seg2_max_time float, seg3_min_time float, seg3_max_time float)")
        cursorObj.execute("INSERT INTO segment_times(total_min_time, total_max_time, seg1_min_time, seg1_max_time, seg2_min_time, seg2_max_time, seg3_max_time, seg3_min_time) VALUES (41.91, 60.32, 17.16, 23.56, 15.14, 25.90, 10.43, 13.34)") # Valors principals
        self.__con.commit()  


    def get_users(self):
        if(self.__con == None):
            return [] # Retornem una llista buida ja que si la connexió és "None", no existeix la BD
        else:
            cursorObj = self.__con.cursor()
            cursorObj.execute("SELECT DNI FROM users WHERE isActive = 1")

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
        cursorObj.execute("UPDATE users SET isActive = 0 WHERE DNI = '"+dni+"'")
        self.__con.commit()
        return True

    def delete_patient(self, dni, table):
        cursorObj = self.__con.cursor()
        cursorObj.execute("DELETE FROM patients WHERE DNI = '"+dni+"'")
        self.__con.commit()

    def set_new_doctor(self, doctor, patient):
        cursorObj = self.__con.cursor()
        cursorObj.execute("UPDATE patients SET doctor = ? WHERE DNI = ?", (doctor, patient))
        self.__con.commit()

    def get_patients_no_doctor(self):
        cursorObj = self.__con.cursor()
        cursorObj.execute("SELECT * FROM patients WHERE doctor in (select dni from users where isActive = 0)")
        return cursorObj.fetchall()

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

    def get_patient_name(self, doctor_dni, patient):
        """
        Retorna els nom del pacient donat el dni del pacient i el seu metge

        Entrada:
            doctor_dni (string): Dni del metge
            patient (string): Dni del pacient
        
        Eixida:
            (patient_full_name): Nom complet del pacient
        """
        cursorObj = self.__con.cursor()
        cursorObj.execute("SELECT name, surname FROM patients where doctor = '"+doctor_dni+"' and dni = '"+patient+"'")
        rows = cursorObj.fetchall()
        return rows[0][0]+" "+rows[0][1]

    def add_patient(self, dni, name, surname, doctor, address, tel, mail, sip, height, weight, birth_date, gender, diag_date, phase, imc, fat, med, face_photo, body_photo):
        """
        Afegeix un pacient

        Entrada:
            dni (string): DNI del pacient
            name (string): nom del pacient
            surname (string): cognom del pacient
            doctor (string): dni del doctor al que s'asociarà eixe pacient
        """
        cursorObj = self.__con.cursor()
        cursorObj.execute("INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (dni, name, surname, doctor, address,
                                                                                                                 tel, mail, sip, height, weight, 
                                                                                                                 birth_date, get_gender(gender), diag_date, phase, imc, 
                                                                                                                 fat, med, face_photo, body_photo))
        self.__con.commit()

    def edit_patient(self, dni, name, surname, doctor, address, tel, mail, sip, height, weight, birth_date, gender, diag_date, phase, imc, fat, med, face_photo, body_photo):

        cursorObj = self.__con.cursor()
        cursorObj.execute("DELETE FROM patients WHERE DNI = '"+dni+"'")
        self.__con.commit()
        self.add_patient(dni, name, surname, doctor, address,
                         tel, mail, sip, height, weight, 
                         birth_date, get_gender(gender), diag_date, phase, imc, 
                         fat, med, face_photo, body_photo)
        
    
    
    
    def get_patient_data(self, dni):
        cursorObj = self.__con.cursor()
        return cursorObj.execute("SELECT * FROM patients WHERE dni = '"+dni+"'").fetchall()[0]
        
    
    def save_lap_times(self, lap_times, patient):
        """
        Guarda els temps asociat al pacient

        Entrada:
            lap_times (float list) Llista de longitud 3 en la que estàn guardades les 3 laps
            patient (string) DNI del pacient al que se li guarda el temps de volta
        """
        cursorObj = self.__con.cursor()
        cursorObj.execute("INSERT INTO times VALUES(?, datetime('now'), ?, ?, ?, (select max(ID) from segment_times))", (patient, lap_times[0], lap_times[1], lap_times[2]))
        self.__con.commit()

    def get_patient_total_times(self, patient):
        """
        Retorna una llista amb el temps total de cada prova cronometrada que se li ha fet

        Entrada:
            patient (string): DNI del pacient del que es vol saber el temps
        Eixida:
            (float list): Llista en la que estàn tots els temps
        """
        cursorObj = self.__con.cursor()
        rows = cursorObj.execute("SELECT lap1, lap2, lap3 from times where patient = '"+patient+"'")
        total_lap_times = []
        for row in rows:
            total_lap_times.append(round(row[0]+row[1]+row[2], 2))
        return total_lap_times

    def get_patient_segment_times(self, patient, seg):
        cursorObj = self.__con.cursor()
        rows = cursorObj.execute("SELECT "+seg+" from times where patient = '"+patient+"'")
        total_seg_times = []
        for row in rows:
            total_seg_times.append(round(float(row[0]), 2))
        return total_seg_times

    def get_patient_dates(self, patient):
        """
        Retorna les dates dels pacients 

        Entrada: 
            patient (string): DNI del pacient del que es vol saber les dades

        Eixida:
            (integer list): Llista de vegades que el pacient ha sigut cronometrat
        """
        cursorObj = self.__con.cursor()
        rows = cursorObj.execute("SELECT day from times where patient = '"+patient+"'")
        days = []
        count = 0
        for row in rows:
            days.append(count)
            count += 1
        return days

    def get_patient_times(self, patient):
        cursorObj = self.__con.cursor()
        cursorObj.execute("SELECT day, lap1, lap2, lap3 from times where patient = '"+patient+"' order by day desc")
        rows = list(cursorObj.fetchall())
        count = 0
        for row in rows:
            rows[count] = list(row)
            rows[count].append(rows[count][1]+rows[count][2]+rows[count][3])
            count += 1
        return rows

    def get_segment_time(self, segment, seg_id=-1):
        if (seg_id == -1):
            seg_id = "(select max(ID) from segment_times)"
        cursorObj = self.__con.cursor()
        rows = cursorObj.execute("SELECT "+segment+" from segment_times where ID = "+seg_id)
        return cursorObj.fetchall()[0][0]

    def get_segment_id(self, patient):
        cursorObj = self.__con.cursor()
        cursorObj.execute("SELECT reference_times from times where patient = '"+patient+"'")
        return cursorObj.fetchall()[0][0]

    def set_new_segments_time(self, times):
        cursorObj = self.__con.cursor()
        cursorObj.execute("""INSERT INTO segment_times(total_min_time, total_max_time, seg1_min_time, seg1_max_time, seg2_min_time, seg2_max_time, seg3_min_time, seg3_max_time)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", times) # Valors principals
        self.__con.commit()


    def close(self):
        """
        Tanca la connexió
        """
        self.__con.close

    def database_exists(self):
        """
        Funció que comprova si el fitxer existeix o no

        Eixida:
            (boolean) Si existeix o no
        """
        return file_exists(self.DB)

def get_gender(gender):
        if(gender):
            return "M"
        return "F"