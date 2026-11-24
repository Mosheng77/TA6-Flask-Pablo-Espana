@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
    py -3 -m venv .venv
    if errorlevel 1 goto error
)
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
echo Abre http://127.0.0.1:5000 en tu navegador.
.venv\Scripts\python.exe main.py
pause
exit /b
:error
echo No se pudo preparar el entorno. Verifica que Python este instalado y tengas Internet.
pause
