@echo off
chcp 65001 > nul
echo Running China Weather Wind Flow Wallpaper Program Step by Step...
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
python -c "import sys; sys.exit(0 if all(m in sys.modules or __import__(m) for m in ['requests', 'PIL', 'selenium', 'schedule']) else 1)" > nul 2>&1
if %errorlevel% neq 0 (
    echo Some dependencies are missing. Installing now...
    pip install requests Pillow selenium schedule
    if %errorlevel% neq 0 (
        echo Failed to install dependencies. Please run 'pip install requests Pillow selenium schedule' manually.
        pause
        exit /b 1
    )
    echo Dependencies installed successfully.
)

echo.
echo ========================================
echo STEP 1: Test fetching wind data
echo ========================================
echo This will test if we can fetch wind flow data from the website.
echo.
set /p continue=Press Enter to continue or type 'skip' to skip this step: 
if /i "%continue%"=="skip" goto step2

python test_fetch_wind_data.py
if %errorlevel% neq 0 (
    echo Test failed. Please check the error messages above.
    set /p continue=Press Enter to continue anyway or Ctrl+C to exit: 
)

:step2
echo.
echo ========================================
echo STEP 2: Test wallpaper setting
echo ========================================
echo This will test if we can set a wallpaper on your system.
echo.
set /p continue=Press Enter to continue or type 'skip' to skip this step: 
if /i "%continue%"=="skip" goto step3

python test_wallpaper_setting.py
if %errorlevel% neq 0 (
    echo Test failed. Please check the error messages above.
    set /p continue=Press Enter to continue anyway or Ctrl+C to exit: 
)

:step3
echo.
echo ========================================
echo STEP 3: Run the full program
echo ========================================
echo This will run the complete program with step-by-step guidance.
echo.
set /p continue=Press Enter to continue or type 'skip' to skip this step: 
if /i "%continue%"=="skip" goto end

python src/wind_wallpaper_new.py

:end
echo.
echo All steps completed.
pause
