@echo off
echo ========================================
echo     DEBUG PROBLEMA PAZIENTI IN ATTESA
echo ========================================
echo.

cd /d "%~dp0"

echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo.
echo Installazione dipendenza requests se necessaria...
pip install requests >nul 2>&1

echo.
echo Esecuzione debug...
python debug_pazienti.py

echo.
echo ========================================
echo     DEBUG COMPLETATO
echo ========================================
echo.
echo Premi un tasto per continuare...
pause > nul