@echo off
echo ============================================
echo    TEST CONNESSIONE BACKEND FLASK
echo ============================================
echo.

echo Controllo se il backend e' in esecuzione...
echo.

REM Test con curl se disponibile
curl --version >nul 2>&1
if %errorlevel% == 0 (
    echo Testando endpoint con curl...
    echo.
    
    echo 1. Test endpoint /api/beds:
    curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:5000/api/beds
    echo.
    
    echo 2. Test endpoint /api/maintenance/staff:
    curl -s -w "Status: %%{http_code}\n" http://localhost:5000/api/maintenance/staff
    echo.
    
    echo 3. Contenuto endpoint personale:
    curl -s http://localhost:5000/api/maintenance/staff
    echo.
    
) else (
    echo curl non disponibile, usando PowerShell...
    echo.
    
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5000/api/beds' -TimeoutSec 5; Write-Host 'Backend ATTIVO - Status:' $response.StatusCode } catch { Write-Host 'Backend NON ATTIVO - Errore:' $_.Exception.Message }"
    echo.
    
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5000/api/maintenance/staff' -TimeoutSec 5; Write-Host 'Endpoint personale - Status:' $response.StatusCode; Write-Host 'Contenuto:'; $response.Content } catch { Write-Host 'Errore endpoint personale:' $_.Exception.Message }"
)

echo.
echo ============================================
echo Se vedi errori di connessione:
echo 1. Esegui 'quick_start.bat' per avviare il backend
echo 2. Aspetta che appaia 'Running on http://127.0.0.1:5000'
echo 3. Riprova questo test
echo ============================================
echo.
pause