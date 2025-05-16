@echo off
:: Configuración inicial
set PROJECT_DIR=./proyecto
set PORT=8000
set VENV_NAME=.venv

call %VENV_NAME%\Scripts\activate
:: Navegar al directorio del proyecto
cd %PROJECT_DIR%

:: Verificar si manage.py existe
if not exist manage.py (
    echo No se encontró el archivo manage.py en %PROJECT_DIR%.
    echo Asegúrate de estar en el directorio correcto.
    pause
    exit /b 1
)

:: Actualizar la base de datos
echo Creando migraciones...
python manage.py makemigrations
if errorlevel 1 (
    echo Error al crear migraciones. Revisa los modelos o las configuraciones.
    pause
    exit /b 1
)

echo Aplicando migraciones...
python manage.py migrate
if errorlevel 1 (
    echo Error al aplicar migraciones. Revisa las configuraciones de la base de datos.
    pause
    exit /b 1
)

:: Iniciar el servidor de desarrollo
echo Iniciando el servidor de Django en el puerto %PORT%...
python manage.py runserver %PORT%
if errorlevel 1 (
    echo Error al iniciar el servidor. Revisa la configuración de tu proyecto.
    pause
    exit /b 1
)

:: Finalización
pause