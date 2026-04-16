@echo off
REM Abre Chrome en modo debug para que Selenium pueda conectarse
REM sin cerrar tu sesión de WhatsApp Web
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
    --remote-debugging-port=9223 ^
    --user-data-dir="C:\selenium\chrome-profile"
