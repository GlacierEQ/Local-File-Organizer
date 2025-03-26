@echo off
echo Installing Bender Rodriguez System Service...
echo.

REM Check for administrative privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Error: Administrative privileges required!
    echo Please run this script as Administrator.
    pause
    exit /b 1
)

REM Create Bender's home directory
echo Creating Bender's home directory...
mkdir "%USERPROFILE%\.bender" 2>nul
mkdir "%USERPROFILE%\.bender\logs" 2>nul
mkdir "%USERPROFILE%\.bender\memory" 2>nul
mkdir "%USERPROFILE%\.bender\models" 2>nul

REM Install Python dependencies
echo Installing Python dependencies...
python -m pip install -r requirements_ai.txt
if %errorLevel% neq 0 (
    echo Error: Failed to install dependencies!
    pause
    exit /b 1
)

REM Install the Windows service
echo Installing Bender service...
python system_service/bender_service.py install
if %errorLevel% neq 0 (
    echo Error: Failed to install service!
    pause
    exit /b 1
)

REM Start the service
echo Starting Bender service...
net start BenderService
if %errorLevel% neq 0 (
    echo Error: Failed to start service!
    pause
    exit /b 1
)

echo.
echo Bender Rodriguez has been successfully installed!
echo You can access his web interface at: http://localhost:5000
echo.
echo "Bite my shiny metal ASCII!"
echo.
pause
