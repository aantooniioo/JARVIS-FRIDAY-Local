@echo off
cd /d "C:\Users\anton\Desktop\J.A.R.V.I.S"
python local_friday.py
if errorlevel 1 (
    echo.
    echo Error al ejecutar Friday. Presiona una tecla para cerrar...
    pause >nul
)
