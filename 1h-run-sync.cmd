@echo off
:loop
powershell ./main.ps1
python upload.py
timeout /t 3600 /nobreak >nul
goto loop
