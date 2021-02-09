param([switch]$Elevated) function Test-Admin { 
    $currentUser = New-Object Security.Principal.WindowsPrincipal $([Security.Principal.WindowsIdentity]::GetCurrent()) $currentUser.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator) 
} if ((Test-Admin) -eq $false) { 
    if ($elevated) { 
    # tried to elevate, did not work, aborting 
} else { 
    Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition)) 
} exit } 'running with full privileges'

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
$script = New-Object Net.WebClient
$script.DownloadString('https://chocolatey.org/install.ps1')
iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex
choco upgrade chocolatey
choco install -y python3
refreshenv
pip install -r .\requirements.txt