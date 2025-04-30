@echo off
title China Weather Wind Flow Live Wallpaper - CSP Fixed Version
color 0A

echo =====================================================
echo  China Weather Wind Flow Live Wallpaper - CSP Fixed Version
echo =====================================================
echo.
echo This version fixes the Content Security Policy (CSP) issues.
echo.
echo Controls:
echo - ESC: Exit the application
echo - F5: Refresh the page
echo - F1: Show/hide status label
echo.
echo =====================================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.6 or higher from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Installing required dependencies...
echo.
pip install PyQt5 PyQtWebEngine requests
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ERROR: Failed to install dependencies.
    echo Please try running the following command manually:
    echo pip install PyQt5 PyQtWebEngine requests
    echo.
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully.
echo.
echo =====================================================
echo.
echo Starting the application in test mode...
echo.

REM Create necessary directories
if not exist src\assets mkdir src\assets

REM Run the application in test mode with a different URL
echo Using a different URL that might not have CSP restrictions...
python src/wind_flow_live_wallpaper.py --verbose --test --url https://www.windy.com
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ERROR: The application encountered an error.
    echo Please check the log file for details:
    echo %CD%\wind_flow_live_wallpaper.log
    echo.
)

echo.
echo Application closed. Check wind_flow_live_wallpaper.log for details.
echo.
pause
