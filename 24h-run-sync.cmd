@echo off
:loop
powershell ./main.ps1
powershell ./upload.ps1
timeout /t 86400 /nobreak >nul
goto loop
