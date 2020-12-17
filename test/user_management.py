import create_user
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import patient_management
import database_manager as sqlite
import chrono
from __manifest__ import path_separator, load_properties, comprobation_message

class Users_management(QtWidgets.QMainWindow):
    def __init__(self):
        super(Users_management, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'users.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.deleteUser.clicked.connect(self.delete_user)
        self.changePass.clicked.connect(self.change_pass)
        self.newUser.clicked.connect(self.create_user)
        self.refreshList.clicked.connect(self.refresh_list)
        self.pacientesIcon.clicked.connect(self.open_patients_menu)

        config = load_properties()
        self.current_user = config.get('UsersSection', 'currentUser')

        self.model = QtGui.QStandardItemModel()
        self.usersList.setModel(self.model)
        self.usersList.clicked.connect(self.manage_user)

        

        self.refresh_list()
        self.dni = ""

        sql_con = sqlite.sqlite_connector()
        if(sql_con.is_admin(self.current_user)):
            self.newUser.show()
        else:
            self.newUser.hide()
        sql_con.close()

        self.cronIcon.clicked.connect(self.return_to_chrono)
        
        
        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color: #fdfdff}")
        self.barraLateral.setStyleSheet("QWidget#barraLateral{ background-color: #555860; }")
        self.cronIcon.setStyleSheet("QPushButton#cronIcon::hover{ border: none; background-color: #a2adc2;} QPushButton#cronIcon::pressed{background-color: #222628;}")
        self.users.setStyleSheet("QPushButton#users::hover{ border: none; background-color: #a2adc2;} QPushButton#users::pressed{background-color: #222628;}")
        self.pacientesIcon.setStyleSheet("QPushButton#pacientesIcon::hover{ border: none; background-color: #a2adc2;} QPushButton#pacientesIcon::pressed{background-color: #222628;}")
        

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def manage_user(self, index):
        self.dni = self.model.itemFromIndex(index).text()
        sql_con = sqlite.sqlite_connector()
        if(sql_con.is_admin(self.current_user) or self.dni == self.current_user):
            self.changePass.show()
        else:
            self.changePass.hide()    

        if(sql_con.is_admin(self.current_user)):
            self.deleteUser.show()
        else:
            self.deleteUser.hide()
        
        sql_con.close()

    def create_user(self):
        self.new_window = create_user.Create_user()

    def change_pass(self):
        sql_con = sqlite.sqlite_connector()
        acces_granted = sql_con.is_admin(self.current_user)
        if(not acces_granted): # Si no és admin i no és ell mateix
            last_passwd, ok = QtWidgets.QInputDialog.getText(self, 'Identifícate', 'Introduzca su contraseña actual, '+self.dni, QtWidgets.QLineEdit.Password)
            if ok:
                if(not sql_con.login(self.dni, last_passwd)): # SI L'AUTENTICACIÓ NO ÉS CORRECT
                    QtWidgets.QMessageBox.critical(self, 'ERROR', "Contraseña incorrecta.")
                    sql_con.close()
                    return
                else:
                    acces_granted = True
            else:
                sql_con.close()
                return
       
        valid_password = False
        while(not valid_password):
            passwd, ok = QtWidgets.QInputDialog.getText(self, 'Cambio de contraseña para usuario '+self.dni, 'Introduzca la nueva contraseña: (8 carácteres o más)', QtWidgets.QLineEdit.Password)
            if ok:
                if(len(passwd) < 8):
                    QtWidgets.QMessageBox.critical(self, 'ERROR', "La contraseña debe ser de 8 carácteres o más")
                else:
                    valid_password = True
            else:
                sql_con.close()
                return
        sql_con.change_password(self.dni, passwd)
        QtWidgets.QMessageBox.information(self, 'Contraseña actualizada', "¡La contraseña ha sido actualizada con éxito!")
        sql_con.close()


    def delete_user(self):
        if self.current_user == self.dni: # Arreglar aço
            QtWidgets.QMessageBox.critical(self, 'ERROR', "No puedes eliminar tu propio usuario.")
        else:
            if comprobation_message('Comprobación', '¿Estás seguro de querer eliminar al usuario '+self.dni+'?'):
                sql_con = sqlite.sqlite_connector()
                if(sql_con.delete_user(self.dni)):
                    QtWidgets.QMessageBox.information(self, 'Confirmación', "El usuario ha sido eliminado con éxito.")
                    self.refresh_list()
                else:
                    QtWidgets.QMessageBox.critical(self, 'ERROR', "El usuario no puede eliminarse porque es el único administrador.")
                sql_con.close()

    def refresh_list(self):
        self.model.removeRows(0, self.model.rowCount()) # Esborra tot
        self.changePass.hide()
        self.deleteUser.hide()
        self.show_users()

    def show_users(self):
        users = sqlite.sqlite_connector().get_users()
        for user in users:
            row = QtGui.QStandardItem(user[0])
            self.model.appendRow(row)

    def return_to_chrono(self):
        self.new_window = chrono.Chrono()
        self.new_window.show()
        self.close()

    def open_patients_menu(self):
        self.new_window = patient_management.Patient_management()
        self.close()