from PyQt5 import QtWidgets, uic, QtCore, QtGui
from __manifest__ import load_properties, comprobation_message, salir
import database_manager as sqlite
import user_management
from os.path import dirname, join
import edit_patient
import chrono
import settings
import create_patient

class Patient_management(QtWidgets.QMainWindow):
    def __init__(self):
        super(Patient_management, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(join(dirname(__file__), 'UI/pacientes.ui'), self) # Load the .ui file
        self.showMaximized() # Show the GUI

        self.nuevoPaciente.clicked.connect(self.new_patient)
        self.borrarPaciente.clicked.connect(self.delete_patient)
        self.editarPaciente.clicked.connect(self.editar_paciente)
        self.refreshList.clicked.connect(self.refresh_list)
        self.editarPaciente.hide()
        self.borrarPaciente.hide()


        

        self.model = QtGui.QStandardItemModel()
        self.listaPacientes.setModel(self.model)
        self.listaPacientes.clicked.connect(self.manage_patient)

        config = load_properties()
        self.current_user = config.get('UsersSection', 'currentUser')

        self.check_patients_without_doctor()

        self.settingsIcon.clicked.connect(self.open_settings)

        self.patients_dni = []
        
        self.refresh_list()
        self.patient_item = ""

        self.borrarPaciente.setStyleSheet("QPushButton#borrarPaciente{ border: 2px solid #717987; font-weight: bold; color: white; background-color: #a2adc2; } QPushButton#borrarPaciente::hover{ background-color: #BDC5D4;} QPushButton#borrarPaciente::pressed{background-color: #717987;}")
        self.editarPaciente.setStyleSheet("QPushButton#editarPaciente{ border: 2px solid #717987; font-weight: bold; color: white; background-color: #a2adc2; } QPushButton#editarPaciente::hover{ background-color: #BDC5D4;} QPushButton#editarPaciente::pressed{background-color: #717987;}")
        self.nuevoPaciente.setStyleSheet("QPushButton#nuevoPaciente{ border: 2px solid #717987; font-weight: bold; color: white; background-color: #a2adc2; } QPushButton#nuevoPaciente::hover{ background-color: #BDC5D4;} QPushButton#nuevoPaciente::pressed{background-color: #717987;}")
        self.refreshList.setStyleSheet("QPushButton#refreshList{ border: 2px solid #717987; font-weight: bold; color: white; background-color: #a2adc2; } QPushButton#refreshList::hover{ background-color: #BDC5D4;} QPushButton#refreshList::pressed{background-color: #717987;}")


        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color: #fdfdff}")
        self.barraLateral.setStyleSheet("QWidget#barraLateral{ background-color: #555860; }")
        self.cronIcon.setStyleSheet("QPushButton#cronIcon::hover{ border: none; background-color: #a2adc2;} QPushButton#cronIcon::pressed{background-color: #222628;}")
        self.users.setStyleSheet("QPushButton#users::hover{ border: none; background-color: #a2adc2;} QPushButton#users::pressed{background-color: #222628;}")
        self.pacientesIcon.setStyleSheet("QPushButton#pacientesIcon::hover{ border: none; background-color: #a2adc2;} QPushButton#pacientesIcon::pressed{background-color: #222628;}")
        self.settingsIcon.setStyleSheet("QPushButton#settingsIcon::hover{ border: none; background-color: #a2adc2;} QPushButton#settingsIcon::pressed{background-color: #222628;}")

        self.cronIcon.clicked.connect(self.return_to_chrono)
        self.users.clicked.connect(self.open_users_menu)
    
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def manage_patient(self, index):
        
        self.patient_item = self.model.itemFromIndex(index)
        self.borrarPaciente.show()
        self.editarPaciente.show()
        

    def editar_paciente(self):
        self.new_window = edit_patient.Edit_patient(self.patients_dni[self.model.indexFromItem(self.patient_item).row()], doctor=self.current_user)
        
    def refresh_list(self):
        self.model.removeRows(0, self.model.rowCount()) # Esborra tot
        self.listaPacientes.setModel(self.model)
        self.show_patients()

    def show_patients(self):
        sql_con = sqlite.sqlite_connector()
        patients = sql_con.get_patient_names(self.current_user)
        self.patients_dni = []
        for patient in patients:
            self.patients_dni.append(patient[2]) # Guardem el DNI de l'usuari
            self.model.appendRow(QtGui.QStandardItem(patient[0]+" "+patient[1]))
        sql_con.close()


    def new_patient(self):
        self.new_window = create_patient.Create_patient(self.current_user)
        

    def check_patients_without_doctor(self):
        sql_con = sqlite.sqlite_connector()
        patients_without_doctor = sql_con.get_patients_no_doctor()
        sql_con.close()
        for patient in patients_without_doctor:
            if comprobation_message('Paciente sin médico', 'El paciente '+patient[1]+" "+patient[2]+' ('+patient[0]+'), no tiene ningún médico asignado ya que el que tenía se ha eliminado. ¿Quieres añadirle un nuevo médico ahora?'):
                self.new_window = edit_patient.Edit_patient(patient[0], True)
        
    def delete_patient(self):
        if comprobation_message('Comprobación', '¿Estás seguro de querer eliminar al paciente '+self.patient_item.text()+' (DNI: '+self.patients_dni[self.model.indexFromItem(self.patient_item).row()]+')?'):
            sql_con = sqlite.sqlite_connector()
            sql_con.delete_patient(self.patients_dni[self.model.indexFromItem(self.patient_item).row()])
            sql_con.close()
            QtWidgets.QMessageBox.information(self, 'Confirmación', "El paciente ha sido eliminado con éxito.")
            self.refresh_list()
            self.borrarPaciente.hide()
            self.editarPaciente.hide()

    def return_to_chrono(self):
        self.new_window = chrono.Chrono()
        self.setVisible(False)
        self.close()
    
    def open_users_menu(self):
        self.new_window = user_management.Users_management()
        self.setVisible(False)
        self.close()

    def open_settings(self):
        self.new_window = settings.Settings()
    
    def closeEvent(self, event):
        if(self.isVisible()):
            if(salir()):
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()