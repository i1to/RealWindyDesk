@echo off
chcp 65001 > nul
echo Running China Weather Wind Flow Viewer...
echo.
echo This application will display the real-time wind flow map from China Weather website.
echo.
echo Controls:
echo - ESC: Exit fullscreen or close the application
echo - F5: Refresh the wind flow data
echo - F11: Toggle fullscreen mode
echo.
echo Installing required dependencies...
pip install PyQt5 selenium Pillow

echo.
echo Starting the application...
python src/wind_flow_viewer.py
echo.
echo Application closed. Check wind_flow_viewer.log for details.
echo.
pause
