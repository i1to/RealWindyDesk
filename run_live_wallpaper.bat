@echo off
chcp 65001 > nul
title China Weather Wind Flow Live Wallpaper
color 0A

echo =====================================================
echo  China Weather Wind Flow Live Wallpaper
echo =====================================================
echo.
echo This application will display the real-time wind flow map
echo from China Weather website as your desktop background.
echo.
echo Controls:
echo - ESC: Exit the application
echo - F5: Refresh the page
echo - F1: Show/hide status label
echo.
echo =====================================================
echo.

REM 检查Python是否已安装
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
pip install PyQt5 PyQtWebEngine Pillow
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ERROR: Failed to install dependencies.
    echo Please try running the following command manually:
    echo pip install PyQt5 PyQtWebEngine Pillow
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
echo The application will appear as a transparent window on your desktop.
echo It may take a few moments to load the website.
echo.
echo If you don't see anything, check the log file:
echo %CD%\wind_flow_live_wallpaper.log
echo.
echo Press Ctrl+C to stop the application if needed.
echo =====================================================
echo.

REM 创建必要的目录
if not exist src\assets mkdir src\assets

REM 运行应用程序
python src/wind_flow_live_wallpaper.py
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ERROR: The application encountered an error.
    echo Please check the log file for details:
    echo %CD%\wind_flow_live_wallpaper.log
    echo.
)

echo.
echo Application closed.
echo.
pause
