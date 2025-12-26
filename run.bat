@echo off
REM Change directory to the folder where this script is located
cd /d "%~dp0"

REM Activate the virtual environment
call venv\Scripts\activate

REM Run the python script
python auto_caption.py

REM Keep the window open to see the output or errors
pause