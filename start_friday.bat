@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "C:\Users\anton\Desktop\J.A.R.V.I.S"
python local_friday.py
if errorlevel 1 (
    echo.
    echo Error al ejecutar Friday. Presiona una tecla para cerrar...
    pause >nul
)
