@echo off
chcp 65001 > nul
title China Weather Wind Flow Live Wallpaper - Test Mode
color 0A

echo =====================================================
echo  China Weather Wind Flow Live Wallpaper - Test Mode
echo =====================================================
echo.
echo This will run the application in test mode, which means:
echo - It will appear as a normal window, not as desktop background
echo - You can move, resize, and close the window normally
echo - All debug information will be displayed in the console
echo.
echo This mode is useful for testing and debugging.
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
pip install PyQt5 PyQtWebEngine requests

echo.
echo Dependencies installed successfully.
echo.
echo =====================================================
echo.
echo Starting the application in test mode...
echo.

REM 创建必要的目录
if not exist src\assets mkdir src\assets

REM 运行应用程序（测试模式）
python src/wind_flow_live_wallpaper.py --verbose --test

echo.
echo Application closed. Check wind_flow_live_wallpaper.log for details.
echo.
pause
