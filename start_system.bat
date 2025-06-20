@echo off
echo Avvio sistema ospedaliero...
echo.

echo Installazione dipendenze...
python -m pip install Flask==2.3.2 Flask-SQLAlchemy==3.0.3 Flask-CORS==4.0.0 python-dotenv==1.0.0

echo.
echo Avvio backend...
cd src\backend
python app.py

echo.
echo Se ci sono errori, controlla i log sopra.
pause
