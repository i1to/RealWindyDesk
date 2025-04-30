@echo off
chcp 65001 > nul
echo Running China Weather Wind Flow Live Wallpaper...
echo.
echo This application will display the real-time wind flow map from China Weather website as your desktop background.
echo.
echo Controls:
echo - ESC: Exit the application
echo - F5: Refresh the page
echo - F1: Show/hide status label
echo.
echo Installing required dependencies...
pip install PyQt5 PyQtWebEngine

echo.
echo Starting the application...
echo The application will appear as a transparent window on your desktop.
echo.
python src/wind_flow_live_wallpaper.py
echo.
echo Application closed. Check wind_flow_live_wallpaper.log for details.
echo.
pause
