# Index de noms

## Login

Input username: **user** \
Input password: **passwd** \
Button: **loginButton** \
Label: **errorLabel** \
Main color: #3564b8 \
Settings icon: **settingsIcon**

## New User

Input username: **user** \
Input password: **passwd** \
Button: **newUserButton** \
Label: **errorLabel** \
Is admin?: **adminCheck**

## New Patient

LineEdit DNI: **dni** \
LineEdit Nom: **nom** \
LineEdit Cognom: **cognom** \
LineEdit direccio: **direccio** \
LineEdit tel: **telefon** \
LineEdit mail: **mail** \
LineEdit: **sip** \
LineEdit altura: **altura** \
LineEdit pes: **pes** \
QDateEdit data naiximent: **naiximent** \
RadioButton hombre: **hombre** \
QDateEdit diagnostic: **diagnostic** \
QComboBox fase de l'enfermetat: **fase** \
LineEdit IMC: **imc** \
LineEdit grasa corporal: **grasa** \
LineEdit medicacio: **medicacio** \
Qlabel foto cara: **fotoCara** \
Qlabel foto cuerpo: **fotoCuerpo** \
Button: **newPatientButton**

## Pacientes

QPushButton añadir nuevo paciente: **nuevoPaciente** \
QPushButton eliminar paciente: **borrarPaciente** \
ListView Lista de los pacientes: **listaPacientes** \
QPushButton para acceder a pacientes desde la barra de la izquierda: **pacientesIcon** \
Qpuhsbutton para refrescar la lista de pacientes: **refreshList**

## Base de dades

user: `prova` \
password: `prova`

## Cronometro

Label cronometro: **cronNum** \
QPushButton Start y Stop: **startStop** \
QPushButton Vueltas: **lap** \
Lista laps: **lapsList** \
Lista menu: **listaMenu** \
ComboBox pacientes: **comboPatients** \
Widget graficas: **graph** \
QPushButton info paciente: **moreInfo** \
QPushButton settings **settingsIcon**

## Ajustes

QLineEdit segmento1: **seg1** \
QLineEdit segmento2: **seg2** \
QLineEdit segmento3: **seg3** \
QLineEdit tiempo total: **tiempoTotal**

## TODO GENERAL FERRAN

Obligatori:

- (✅) Ordenar gràfica cronológicament (En teoría sols en afegir order by a la sentència deuria estar)
- Poder editar un pacient (Possiblement utilitzem de finestra el createUser)
- (✅) No s'esborra el doctor sino que passa a estat inactiu, però continua a la BD (Quan accedim a la pestanya de pacients, que els comprove tots a veure si hi ha algún amb un metge inactiu, en cas de que hi haja, que ens demane un nou metge per a ell) es guardarà a la BD
- (✅) Si un doctor està donat de baixa, no pot fer login
- (✅) Quan creem un metge, la contrasenya s'ha de ficar dos vegades
- (✅) Mostrar en la gràfica més dades: Lap1, Lap2, Lap3 i temps total.
- (✅) Afegir les noves dades dels pacients aixi com també editar el add patient

Opcional:

- Informe en PDF
- (🔄(Possiblement mes rentable deixar-ho de costat)) Quan es cree un metge o un pacient, que automàticament es refresque la llista
- Calcular la lletra del DNI automàticament
- Quan ens demana introduïr el primer usuari:
    1. Que no ens done l'opció d'afegir un altre
    2. Si ens dona l'opció, que puga ser no-admin
- (🛑) No recalcular del temps del settings els camps quan mostrem el more info, sino que el temps en el que s'ha fet la prova
