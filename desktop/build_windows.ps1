$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\pyinstaller.exe --noconfirm --clean --windowed --name TrueVision --paths . main.py
Write-Host "Built dist\TrueVision\TrueVision.exe"
