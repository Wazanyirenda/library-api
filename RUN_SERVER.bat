@echo off
echo Activating virtual environment...
call env\Scripts\activate.bat
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting server...
python run.py

