@echo off
echo ========================================
echo     AVVIO BACKEND HOSPITAL MANAGEMENT
echo ========================================
echo.

cd /d "%~dp0"

echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo.
echo Cambio directory al backend...
cd src\backend

echo.
echo Avvio del server Flask...
echo Il backend sarà disponibile su: http://localhost:5000
echo.
echo Per fermare il server, premi Ctrl+C
echo.

python app.py

echo.
echo ========================================
echo     BACKEND ARRESTATO
echo ========================================
echo.
pause