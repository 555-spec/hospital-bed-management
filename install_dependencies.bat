@echo off
echo Installazione delle dipendenze Python...
echo.

REM Attiva l'ambiente virtuale se esiste
if exist "venv\Scripts\activate.bat" (
    echo Attivazione ambiente virtuale...
    call venv\Scripts\activate.bat
) else (
    echo Ambiente virtuale non trovato, uso Python globale
)

echo.
echo Installazione dipendenze da requirements.txt...
pip install -r requirements.txt

echo.
echo Installazione completata!
echo.
echo Ora puoi avviare il backend con quick_start.bat
pause