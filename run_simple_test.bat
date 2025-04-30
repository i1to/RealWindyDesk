@echo off
chcp 65001 > nul
echo Running Simple Test for Wind Flow Wallpaper Program...
echo.
echo This script will run a simplified version of the program to test if it works.
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not detected. Please install Python 3.6 or higher.
    pause
    exit /b 1
)

REM Create a simple test script
echo import os > simple_test.py
echo import sys >> simple_test.py
echo import logging >> simple_test.py
echo import traceback >> simple_test.py
echo. >> simple_test.py
echo # Configure logging >> simple_test.py
echo logging.basicConfig( >> simple_test.py
echo     level=logging.DEBUG, >> simple_test.py
echo     format='%%(asctime)s - %%(levelname)s - %%(message)s', >> simple_test.py
echo     handlers=[ >> simple_test.py
echo         logging.FileHandler('test.log', encoding='utf-8'), >> simple_test.py
echo         logging.StreamHandler(sys.stdout) >> simple_test.py
echo     ] >> simple_test.py
echo ) >> simple_test.py
echo. >> simple_test.py
echo logger = logging.getLogger() >> simple_test.py
echo. >> simple_test.py
echo try: >> simple_test.py
echo     logger.info("Starting test...") >> simple_test.py
echo     from PIL import Image, ImageDraw, ImageFont >> simple_test.py
echo     logger.info("PIL imported successfully") >> simple_test.py
echo. >> simple_test.py
echo     # Create a test image >> simple_test.py
echo     img = Image.new("RGB", (100, 100), "blue") >> simple_test.py
echo     img.save("test.bmp") >> simple_test.py
echo     logger.info("Test image created successfully") >> simple_test.py
echo. >> simple_test.py
echo     # Test if we can set wallpaper >> simple_test.py
echo     import ctypes >> simple_test.py
echo     abs_path = os.path.abspath("test.bmp") >> simple_test.py
echo     logger.info(f"Setting wallpaper: {abs_path}") >> simple_test.py
echo     result = ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3) >> simple_test.py
echo     logger.info(f"SystemParametersInfoW result: {result}") >> simple_test.py
echo. >> simple_test.py
echo     # Test if we can import selenium >> simple_test.py
echo     import selenium >> simple_test.py
echo     logger.info(f"Selenium version: {selenium.__version__}") >> simple_test.py
echo. >> simple_test.py
echo     logger.info("All tests passed!") >> simple_test.py
echo except Exception as e: >> simple_test.py
echo     logger.error(f"Test failed: {e}") >> simple_test.py
echo     logger.error(traceback.format_exc()) >> simple_test.py

echo Running simple test...
python simple_test.py
echo.
echo Test completed. Check test.log for details.
echo.
pause
