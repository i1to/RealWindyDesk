@echo off
chcp 65001 > nul

:: Check for admin rights
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else (
    goto GotAdmin
)

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:GotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

:: Run the Python script
echo Running China Weather Wind Flow Wallpaper Program with administrator privileges...
echo.

:: Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not detected. Please install Python 3.6 or higher.
    echo Download URL: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Run the program
python src/wind_wallpaper_new.py

pause
