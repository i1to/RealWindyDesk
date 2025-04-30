@echo off
chcp 65001 > nul
echo Testing China Weather Wind Flow Wallpaper Program...
echo This will test if the program can fetch wind flow data correctly.
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not detected. Please install Python 3.6 or higher.
    echo Download URL: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import requests, PIL, selenium, schedule" > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Some dependencies are missing. Please run 'setup.bat' first.
    pause
    exit /b 1
)

REM Check if ChromeDriver exists
if not exist chromedriver.exe (
    echo Warning: ChromeDriver (chromedriver.exe) not found.
    echo Please download the ChromeDriver that matches your Chrome browser version and place it in the program directory.
    echo Download URL: https://chromedriver.chromium.org/downloads
    echo.
    pause
    exit /b 1
)

REM Run the test
echo Running test...
echo.
python -c "from src.wind_wallpaper_new import fetch_wind_data; timestamp, screenshot_path, _ = fetch_wind_data(); print(f'Test result: {"Success" if timestamp and screenshot_path else "Failed"}')"

echo.
echo If the test was successful, you should see a screenshot file in the program directory.
echo You can now run 'start_wind_wallpaper.bat' to start the program.
echo.
pause
