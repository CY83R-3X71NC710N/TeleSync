@echo off
:loop
python main.py
timeout /t 3600 /nobreak >nul
goto loop
