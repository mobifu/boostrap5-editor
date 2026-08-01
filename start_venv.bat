@echo off
:: Prüfen, ob Admin-Rechte vorhanden sind
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Starte neu als Administrator...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

cd /d "C:\E\python\boostrap5-editor"
call .\.venv\Scripts\activate
cmd
