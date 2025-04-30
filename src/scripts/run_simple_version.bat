@echo off
chcp 65001 > nul
echo Running Simple Version of Wind Flow Wallpaper Program...
echo.
echo This is a simplified version that only creates and sets a basic wallpaper.
echo It will help us test if the basic functionality works.
echo.
echo Press any key to continue...
pause > nul

python src/simple_wind_wallpaper.py
echo.
echo Program execution completed. Check simple_wind_wallpaper.log for details.
echo.
pause
