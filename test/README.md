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

Input DNI: **dni** \
Input Nom: **nom** \
Input Cognom: **cognom** \
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

- Ordenar gràfica cronológicament (En teoría sols en afegir order by a la sentència deuria estar)
- Poder editar el metge i nom d'un pacient
- No s'esborra el doctor sino que passa a estat inactiu, però continua a la BD
- No recalcular del temps del settings els camps quan mostrem el more info, sino que el temps en el que s'ha fet la prova es guardarà a la BD
- Quan creem un pacient, la contrasenya s'ha de ficar dos vegades

Opcional:

- Calcular la lletra del DNI automàticament
- Quan ens demana introduïr el primer usuari:
    1. Que no ens done l'opció d'afegir un altre
    2. Si ens dona l'opció, que puga ser no-admin
