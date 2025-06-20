@echo off
chcp 65001 >nul
echo ========================================
echo     CORREZIONE TIMESTAMP DATABASE
echo ========================================
echo.
echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat
echo.
echo Esecuzione script di correzione...
python fix_timestamps.py
echo.
echo Script completato.
pause