from PyQt5 import QtWidgets, uic, QtCore
from __manifest__ import path_separator, comprobation_message, calculate_imc, check_dni
import database_manager as sqlite
import user_management


class Create_user(QtWidgets.QDialog):
    def __init__(self, first_user=False):
        super(Create_user, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("test"+path_separator+'UI' + path_separator + 'newUser.ui', self)  # Load the .ui file
        self.show()
        self.dni_letters = 'TRWAGMYFPDXBNJZSQVHLCKE'


        self.newUserButton.clicked.connect(self.create_user)

        self.user.textChanged.connect(self.check_dni)
        
        self.first_user = first_user;
        if(self.first_user):
            self.adminCheck.setChecked(True)
            self.adminCheck.toggled.connect(self.set_true)


        #self.newUserButton.clicked.connect(self.create_user)
        self.user.returnPressed.connect(self.create_user)
        self.passwd.returnPressed.connect(self.create_user)
        self.repeat_pass.returnPressed.connect(self.create_user)
        
    def check_dni(self):
        check_dni(self.user, self.dni_letters)
        
        
    def set_true(self):
        if(not self.adminCheck.isChecked()):
            self.adminCheck.setChecked(True)
            QtWidgets.QMessageBox.critical(self, 'Error', "El primer usuario DEBE ser administrador") # Mostrem un missatge emergent d'error
    

    def create_user(self):
        dni = self.user.text()
        passwd = self.passwd.text()
        if (len(dni) < 9):  # Major que 9 no pot ser perque està controlat a l'interfície
            QtWidgets.QMessageBox.critical(self, 'ERROR', "El DNI debe ser de 9 dígitos.")
        elif(self.dni_letters[int(dni[:-1]) % 23] != dni[-1]):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Letra del DNI errónea")
        elif (len(passwd) < 8):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "La contraseña no puede ser menor a 8 carácteres.")
        elif(passwd != self.repeat_pass.text()):
            QtWidgets.QMessageBox.critical(self, 'ERROR', "Las contraseñas no coinciden.")
        else:
            try:
                sql_con = sqlite.sqlite_connector()
                if(self.first_user):
                    sql_con.create_initial_table() # Creem les taules inicials
                sql_con.create_user(dni, passwd, self.adminCheck.isChecked())
                QtWidgets.QMessageBox.information(self, 'Usuario añadido', "¡El usuario ha sido añadido con éxito!")
                if comprobation_message('Añadir otro usuario', '¿Quieres añadir otro usuario?'): # If OK is clicked in the button
                    self.user.setText("")
                    self.passwd.setText("")
                    self.repeat_pass.setText("")
                    try:
                        self.adminCheck.toggled.disconnect(self.set_true)
                    except TypeError:
                        pass
                else:
                    self.close()
            except sqlite.sqlite3.IntegrityError:
                QtWidgets.QMessageBox.critical(self, 'ERROR', "Ya existe un usuario con este DNI")
            finally:
                self.user.setText("")
                self.passwd.setText("")
                self.repeat_pass.setText("")
        