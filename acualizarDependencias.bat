@echo off
:: Configuración inicial
set VENV_NAME=.venv
call echo.

:: Verificar si el entorno virtual existe y activarlo
if exist %VENV_NAME%\Scripts\activate (
    echo Activando el entorno virtual %VENV_NAME%...
    call %VENV_NAME%\Scripts\activate
) else (
    echo No se encontró el entorno virtual "%VENV_NAME%" en el directorio actual.
    echo Asegúrate de tener el entorno virtual creado.
    pause
    exit /b 1
)

:: Generar el archivo requirements.txt con las dependencias instaladas
echo Generando el archivo requirements.txt...
pip freeze > requirements.txt
if errorlevel 1 (
    echo Error al generar el archivo requirements.txt. Asegúrate de que pip esté correctamente instalado.
    pause
    exit /b 1
)

echo El archivo requirements.txt ha sido generado exitosamente.
pause
