@echo off
chcp 65001 > nul
echo Running Wind Flow Wallpaper Program in Non-Interactive Mode...
echo.
echo This will run the program without requiring user input.
echo The program will write detailed logs to wind_wallpaper.log file.
echo.
echo Press Ctrl+C to stop the program.
echo.
echo Starting program...

REM Create a wrapper script that runs the program in non-interactive mode
echo import os > run_wrapper.py
echo import sys >> run_wrapper.py
echo import subprocess >> run_wrapper.py
echo. >> run_wrapper.py
echo # Set environment variable to indicate non-interactive mode >> run_wrapper.py
echo os.environ['NON_INTERACTIVE'] = '1' >> run_wrapper.py
echo. >> run_wrapper.py
echo # Run the program >> run_wrapper.py
echo try: >> run_wrapper.py
echo     print("Starting wind_wallpaper_new.py in non-interactive mode...") >> run_wrapper.py
echo     result = subprocess.run([sys.executable, "src/wind_wallpaper_new.py"], check=True) >> run_wrapper.py
echo     print(f"Program exited with code {result.returncode}") >> run_wrapper.py
echo except subprocess.CalledProcessError as e: >> run_wrapper.py
echo     print(f"Program failed with code {e.returncode}") >> run_wrapper.py
echo except Exception as e: >> run_wrapper.py
echo     print(f"Error: {e}") >> run_wrapper.py

python run_wrapper.py
echo.
echo Program execution completed. Check wind_wallpaper.log for details.
echo.
pause
