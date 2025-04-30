@echo off
title China Weather Wind Flow Map Viewer
color 0A

echo =====================================================
echo  China Weather Wind Flow Map Viewer
echo =====================================================
echo.
echo This application will display the wind flow map from China Weather website
echo as a full screen display, hiding all UI elements.
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
echo Starting the application...
echo.
echo The application will load the China Weather website and
echo automatically switch to the wind flow view.
echo.
echo It may take a few moments to load. Please be patient.
echo.
echo =====================================================
echo.

REM Create necessary directories
if not exist src\assets mkdir src\assets

REM Run the application
python src/wind_flow_map.py --verbose
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ERROR: The application encountered an error.
    echo Please check the log file for details:
    echo %CD%\wind_flow_map.log
    echo.
)

echo.
echo Application closed. Check wind_flow_map.log for details.
echo.
pause
