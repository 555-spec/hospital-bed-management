@echo off
echo ============================================
echo    APERTURA TEST DIAGNOSTICO FRONTEND
echo ============================================
echo.

echo Aprendo il test diagnostico nel browser...
echo.

REM Apri il file HTML nel browser predefinito
start "" "test_frontend.html"

echo.
echo Il test diagnostico dovrebbe aprirsi nel browser.
echo Se non si apre automaticamente:
echo 1. Apri manualmente il file test_frontend.html
echo 2. Oppure vai su: file:///c:/Users/Cinzia%%20Del%%20Fonso/Desktop/hospital-bed-management/test_frontend.html
echo.
echo ============================================
echo ISTRUZIONI:
echo 1. Il test verifichera' automaticamente il backend
echo 2. Se vedi errori di connessione, esegui 'quick_start.bat'
echo 3. Aspetta che il backend si avvii completamente
echo 4. Ricarica la pagina di test
echo ============================================
echo.
pause