@echo off
chcp 65001 >nul
echo ========================================
echo    DIAGNOSI SISTEMA OSPEDALIERO
echo ========================================
echo.
echo Avvio diagnosi completa...
echo.

python diagnose_and_fix.py

echo.
echo Diagnosi completata.
echo.
pause