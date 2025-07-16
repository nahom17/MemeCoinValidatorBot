@echo off
call .venv\Scripts\activate.bat
:loop
python run.py
echo Bot crashed. Restarting in 5 seconds...
timeout /t 5
goto loop