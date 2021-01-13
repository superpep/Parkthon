from PyQt5 import QtWidgets, uic, QtCore
import database_manager as sqlite


import sys


from __manifest__ import calculate_imc, path_separator

class Edit_patient(QtWidgets.QMainWindow):
    def __init__(self, patient_dni="123123123"):
        super(Edit_patient, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI'+path_separator+'newPatient.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.patient_dni = patient_dni
        self.titulo.setText("EDITAR PACIENTE")
        self.set_editable_text(False) # Desactivem la edició

        self.newPatientButton.setText("Editar usuario")
        self.fotoCaraButton.setText("Editar foto")
        self.fotoCuerpoButton.setText("Editar foto")
        self.newPatientButton.clicked.connect(self.edit_mode) 

        self.load_data() # Carreguem les dades

        self.pes.editingFinished.connect(self.write_imc);
        self.altura.editingFinished.connect(self.write_imc)

        

        #self.fotoCaraButton.clicked.connect(self.set_photo_cara)
        #self.fotoCuerpoButton.clicked.connect(self.set_photo_cuerpo)

    

    def load_data(self):
        sql_con = sqlite.sqlite_connector()
        data = sql_con.get_patient_data(self.patient_dni)

        print(data)

        
        self.dni.setText(data[0])
        self.nom.setText(data[1])
        self.cognom.setText(data[2])

        self.naiximent.setDate(QtCore.QDate.fromString(data[10],"dd/MM/yyyy"))
        self.diagnostic.setDate(QtCore.QDate.fromString(data[12],"dd/MM/yyyy"))

        """
        data[11] genere
        data[13] escala
        data[17] BLOB fotocara
        data[18] BLOB fotocuerpo
        
        """
        sql_con.close()
        #TO-DO: Que carregue les dades

    def edit_mode(self):
        self.set_editable_text(True) # Activem la edició

        self.newPatientButton.setText("Guardar")
        self.newPatientButton.clicked.disconnect(self.edit_mode)
        self.newPatientButton.clicked.connect(self.save_edit)
    
    def save_edit(self):
        self.set_editable_text(False) # Desactivem l'edició

        # TO-DO: Que guarde les dades

        self.newPatientButton.setText("Editar usuario")
        self.newPatientButton.clicked.disconnect(self.save_edit)
        self.newPatientButton.clicked.connect(self.edit_mode)

    def write_imc(self):
        self.imc.setText(calculate_imc(self.pes.text(), self.altura.text()))
        self.grasa.setText(self.imc.text()+"%")

    def set_editable_text(self, mode):
        self.dni.setReadOnly(not mode)
        self.nom.setReadOnly(not mode)
        self.cognom.setReadOnly(not mode)
        self.direccio.setReadOnly(not mode)
        self.telefon.setReadOnly(not mode)
        self.mail.setReadOnly(not mode)
        self.sip.setReadOnly(not mode)
        self.altura.setReadOnly(not mode)
        self.pes.setReadOnly(not mode)
        self.naiximent.setReadOnly(not mode)
        self.hombre.setCheckable(mode)
        self.mujer.setCheckable(mode)
        self.diagnostic.setReadOnly(not mode)
        self.medicacio.setReadOnly(not mode)

        if(mode):
            self.fotoCaraButton.show()
            self.fotoCuerpoButton.show()
        else:
            self.fotoCaraButton.hide()
            self.fotoCuerpoButton.hide()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Edit_patient()# Llancem el login
    app.exec_() # Start the application