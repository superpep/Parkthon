Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
$script = New-Object Net.WebClient
$script.DownloadString('https://chocolatey.org/install.ps1')
iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex
choco upgrade chocolatey
choco install --force -y python3
C:\Python39\python.exe -m ensurepip
clear
"PYTHON INSTALADO."
C:\Python39\python.exe -m pip install -r .\requirements.txt
clear
"DEPENDENCIAS INSTALADAS."
C:\Python39\python.exe .\cli.py