@echo off
chcp 65001 > nul
echo Running China Weather Wind Flow Desktop Application...
echo.
echo This application will display the real-time wind flow map from China Weather website.
echo The application will appear as a semi-transparent window on your desktop.
echo.
echo Controls:
echo - ESC: Exit the application
echo - F5: Refresh the wind flow data
echo - F11: Toggle fullscreen mode
echo - Hold Alt: Allow dragging the window
echo.
echo Installing required dependencies...
pip install PyQt5 PyQtWebEngine

echo.
echo Starting the application...
python src/wind_flow_desktop.py
echo.
echo Application closed. Check wind_flow_desktop.log for details.
echo.
pause
