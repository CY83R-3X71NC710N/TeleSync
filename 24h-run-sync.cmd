@echo off
:loop
powershell ./main.ps1
python create-channel.py
python upload.py
timeout /t 86400 /nobreak >nul
goto loop
