@echo off
chcp 65001 > nul
echo Starting China Weather Wind Flow Wallpaper Program...
echo The program will run in the background, you can close this window.
echo To stop the program, end the Python process in Task Manager.
echo.
start /b pythonw src/wind_wallpaper_new.py
echo Program started!
timeout /t 5
