@echo off
:: Check if the script is running as administrator
NET SESSION >NUL 2>&1
IF %ERRORLEVEL% EQU 0 (
    goto loop
) ELSE (
    echo You need to run this script as an administrator
    pause
    exit /b 1
)

cd /d "%~dp0"
:loop
powershell ./main.ps1
python create-channel.py
python upload.py
timeout /t 86400 /nobreak >nul
goto loop
