@echo off
:loop
powershell ./main.ps1
python upload.py
timeout /t 86400 /nobreak >nul
goto loop
