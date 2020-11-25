from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import login
import configparser
import database_manager as sqlite
class Patient_management(QtWidgets.QMainWindow):
    def __init__(self):
        super(Patient_management, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+login.pathSeparator+'pacientes.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.nuevoPaciente.clicked.connect(self.new_patient)
        self.borrarPaciente.clicked.connect(self.delete_patient)

        self.model = QtGui.QStandardItemModel()
        self.listaPacientes.setModel(self.model)
        self.listaPacientes.clicked.connect(self.manage_patient)

        config = configparser.RawConfigParser()
        config.read(sqlite.configFileName)
        self.currentUser = config.get('UsersSection', 'currentUser')

        self.patients_dni = []
        self.sql_con = sqlite.sqlite_connector()
        self.reinicia_llista()
        self.patient_item = ""

        self.centralwidget.setStyleSheet("QWidget#centralwidget{ background-color: #f0f0f0}")
        self.barraLateral.setStyleSheet("QWidget#barraLateral{ background-color: #d6d6d6; }")
        self.cronIcon.setStyleSheet("QPushButton#cronIcon::hover{ border: none; background-color: #EEEEEE;} QPushButton#cronIcon::pressed{background-color: #555555;}")
        self.users.setStyleSheet("QPushButton#users::hover{ border: none; background-color: #EEEEEE;} QPushButton#users::pressed{background-color: #555555;}")
        
    
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def manage_patient(self, index):
        self.patient_item = self.model.itemFromIndex(index)
        
    def reinicia_llista(self):
        self.model.removeRows(0, self.model.rowCount()) # Esborra tot
        self.show_patients()

    def show_patients(self):
        patients = self.sql_con.get_patient_names(self.currentUser)
        for patient in patients:
            self.patients_dni.append(patient[2]) # Guardem el DNI de l'usuari
            self.model.appendRow(QtGui.QStandardItem(patient[0]+" "+patient[1]))

    def new_patient(self):
        pass
    
    def delete_patient(self):
        choice = comprovacio(self.patient_item.text())
        if choice:
            self.sql_con.delete_patient(self.patients_dni[self.model.indexFromItem(self.patient_item).row()])
            QtWidgets.QMessageBox.information(self, 'Confirmación', "El paciente ha sido eliminado con éxito.")
            self.reinicia_llista()

    def return_to_chrono(self):
        self.new_window = chrono.Chrono()
        self.new_window.show()
        self.close()

def comprovacio(patient_name):
    box = QtWidgets.QMessageBox()
    box.setIcon(QtWidgets.QMessageBox.Question)
    box.setWindowTitle('Comprovació')
    box.setText('¿Estás seguro de querer eliminar al paciente '+patient_name+'?')
    box.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
    buttonY = box.button(QtWidgets.QMessageBox.Yes)
    buttonY.setText('Sí')
    buttonN = box.button(QtWidgets.QMessageBox.No)
    buttonN.setText('No')
    box.exec_()
    return box.clickedButton() == buttonY
# Eliminar aço despres de acabar les proves ja que no volem que es puga executar
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Patient_management() # Create an instance of our class
    app.exec_() # Start the application