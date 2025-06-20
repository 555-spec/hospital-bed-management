@echo off
echo ========================================
echo    AVVIO FRONTEND HOSPITAL MANAGEMENT
echo ========================================
echo.

cd /d "%~dp0"

echo Cambio directory al frontend...
cd src\frontend

echo.
echo Controllo dipendenze Node.js...
if not exist node_modules (
    echo Installazione dipendenze npm...
    npm install
) else (
    echo Dipendenze già installate.
)

echo.
echo Avvio del server di sviluppo React...
echo Il frontend sarà disponibile su: http://localhost:3000
echo.
echo Per fermare il server, premi Ctrl+C
echo.

npm start

echo.
echo ========================================
echo     FRONTEND ARRESTATO
echo ========================================
echo.
pause