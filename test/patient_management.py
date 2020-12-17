from PyQt5 import QtWidgets, uic, QtCore, QtGui
from __manifest__ import path_separator, load_properties, comprobation_message
import database_manager as sqlite
import user_management
import chrono
import create_patient

class Patient_management(QtWidgets.QMainWindow):
    def __init__(self):
        super(Patient_management, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'pacientes.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.nuevoPaciente.clicked.connect(self.new_patient)
        self.borrarPaciente.clicked.connect(self.delete_patient)
        self.refreshList.clicked.connect(self.refresh_list)
        self.borrarPaciente.hide()

        self.model = QtGui.QStandardItemModel()
        self.listaPacientes.setModel(self.model)
        self.listaPacientes.clicked.connect(self.manage_patient)

        config = load_properties()
        self.current_user = config.get('UsersSection', 'currentUser')

        self.patients_dni = []
        
        self.refresh_list()
        self.patient_item = ""

        
        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color: #fdfdff}")
        self.barraLateral.setStyleSheet("QWidget#barraLateral{ background-color: #555860; }")
        self.cronIcon.setStyleSheet("QPushButton#cronIcon::hover{ border: none; background-color: #a2adc2;} QPushButton#cronIcon::pressed{background-color: #222628;}")
        self.users.setStyleSheet("QPushButton#users::hover{ border: none; background-color: #a2adc2;} QPushButton#users::pressed{background-color: #222628;}")
        self.pacientesIcon.setStyleSheet("QPushButton#pacientesIcon::hover{ border: none; background-color: #a2adc2;} QPushButton#pacientesIcon::pressed{background-color: #222628;}")
        
        self.cronIcon.clicked.connect(self.return_to_chrono)
        self.users.clicked.connect(self.open_users_menu)
    
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def manage_patient(self, index):
        self.patient_item = self.model.itemFromIndex(index)
        self.borrarPaciente.show()
        
    def refresh_list(self):
        self.model.removeRows(0, self.model.rowCount()) # Esborra tot
        self.show_patients()

    def show_patients(self):
        sql_con = sqlite.sqlite_connector()
        patients = sql_con.get_patient_names(self.current_user)
        for patient in patients:
            self.patients_dni.append(patient[2]) # Guardem el DNI de l'usuari
            self.model.appendRow(QtGui.QStandardItem(patient[0]+" "+patient[1]))
        sql_con.close()


    def new_patient(self):
        self.new_window = create_patient.Create_patient()
    
    def delete_patient(self):
        if comprobation_message('Comprovación', '¿Estás seguro de querer eliminar al paciente '+self.patient_item.text()+'?'):
            sql_con.delete_patient(self.patients_dni[self.model.indexFromItem(self.patient_item).row()])
            sql_con.close()
            QtWidgets.QMessageBox.information(self, 'Confirmación', "El paciente ha sido eliminado con éxito.")
            self.refresh_list()
            self.borrarPaciente.hide()

    def return_to_chrono(self):
        self.new_window = chrono.Chrono()
        self.close()
    
    def open_users_menu(self):
        self.new_window = user_management.Users_management()
        self.close()
