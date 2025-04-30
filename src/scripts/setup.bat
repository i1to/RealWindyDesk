@echo off
chcp 65001 > nul
echo Installing China Weather Wind Flow Wallpaper Program...
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not detected. Please install Python 3.6 or higher.
    echo Download URL: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies. Please check your network connection or run 'pip install -r requirements.txt' manually.
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

REM Check for ChromeDriver
if not exist chromedriver.exe (
    echo Warning: ChromeDriver (chromedriver.exe) not found.
    echo Please download the ChromeDriver that matches your Chrome browser version and place it in the program directory.
    echo Download URL: https://chromedriver.chromium.org/downloads
    echo.
)

echo Installation complete!
echo.
echo Usage:
echo 1. Make sure you have downloaded ChromeDriver and placed it in the program directory
echo 2. Run 'python src/wind_wallpaper_new.py' to start the program
echo.
echo For detailed instructions, please refer to the USAGE_GUIDE.md file
echo.
pause
