@echo off
chcp 65001 > nul
echo Running China Weather Wind Flow Wallpaper Program with Console Window...
echo.
echo This will run the program in a console window so you can see all log messages.
echo The program will also write detailed logs to wind_wallpaper.log file.
echo.
echo Press Ctrl+C to stop the program.
echo.
pause

python src/wind_wallpaper_new.py
pause
