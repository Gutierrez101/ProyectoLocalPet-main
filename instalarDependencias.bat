@echo off
:: Nombre del entorno virtual
set VENV_NAME=.venv
call echo.

:: Verificar si el entorno ya existe
if exist %VENV_NAME% (
    echo El entorno virtual "%VENV_NAME%" ya existe.
) else (
    echo Creando el entorno virtual "%VENV_NAME%"...
    python -m venv %VENV_NAME%
    if errorlevel 1 (
        echo Error al crear el entorno virtual. Asegúrate de que Python esté instalado y configurado en PATH.
        pause
        exit /b 1
    )
    echo Entorno virtual creado con éxito.
)

:: Activar el entorno virtual
echo Activando el entorno virtual...
call %VENV_NAME%\Scripts\activate

:: Verificar si requirements.txt existe
if exist requirements.txt (
    echo Instalando dependencias desde requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error al instalar dependencias. Revisa el archivo requirements.txt.
        pause
        exit /b 1
    )
    echo Dependencias instaladas correctamente.
) else (
    echo No se encontró el archivo "requirements.txt". Por favor, colócalo en el mismo directorio que este script.
)

:: Finalización
echo El entorno virtual está listo para usarse.
echo Para activarlo manualmente, ejecuta: %VENV_NAME%\Scripts\activate
pause
