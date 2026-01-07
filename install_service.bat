@echo off
REM Service Installer for Auto Writer Service
REM This script must be run as Administrator

echo ================================================
echo Auto Writer Service Installer
echo ================================================
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Administrator privileges confirmed.
    echo.
) else (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as Administrator"
    pause
    exit /b 1
)

echo Select an option:
echo 1. Install Service
echo 2. Start Service
echo 3. Stop Service
echo 4. Restart Service
echo 5. Uninstall Service
echo 6. Check Service Status
echo 7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto start
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto restart
if "%choice%"=="5" goto uninstall
if "%choice%"=="6" goto status
if "%choice%"=="7" goto end

echo Invalid choice!
pause
exit /b 1

:install
echo.
echo Installing Auto Writer Service...
python write_service.py install
if %errorLevel% == 0 (
    echo Service installed successfully!
    echo.
    echo You can now start the service using option 2 or with:
    echo   net start AutoWriterService
) else (
    echo Failed to install service. Make sure pywin32 is installed.
    echo   pip install pywin32
)
echo.
pause
goto end

:start
echo.
echo Starting Auto Writer Service...
net start AutoWriterService
if %errorLevel% == 0 (
    echo Service started successfully!
) else (
    echo Failed to start service. Check if it's already running or installed.
)
echo.
pause
goto end

:stop
echo.
echo Stopping Auto Writer Service...
net stop AutoWriterService
if %errorLevel% == 0 (
    echo Service stopped successfully!
) else (
    echo Failed to stop service. Check if it's running.
)
echo.
pause
goto end

:restart
echo.
echo Restarting Auto Writer Service...
net stop AutoWriterService
timeout /t 2 /nobreak >nul
net start AutoWriterService
if %errorLevel% == 0 (
    echo Service restarted successfully!
) else (
    echo Failed to restart service.
)
echo.
pause
goto end

:uninstall
echo.
echo Stopping service first...
net stop AutoWriterService 2>nul
timeout /t 2 /nobreak >nul
echo Uninstalling Auto Writer Service...
python write_service.py remove
if %errorLevel% == 0 (
    echo Service uninstalled successfully!
) else (
    echo Failed to uninstall service.
)
echo.
pause
goto end

:status
echo.
echo Checking service status...
sc query AutoWriterService
echo.
pause
goto end

:end
exit /b 0
