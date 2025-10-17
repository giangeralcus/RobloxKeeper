@echo off
REM Anime Vanguards Keeper - Installation Script
REM Windows Edition

echo ========================================
echo   ANIME VANGUARDS KEEPER INSTALLER
echo ========================================
echo.

REM Check if Python is installed
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python is installed
py --version
echo.

REM Install required packages
echo Installing required packages...
echo.

py -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install packages!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   INSTALLATION COMPLETE!
echo ========================================
echo.
echo You can now run the keeper using:
echo   - Double-click "START_KEEPER.bat"
echo   - Or run: py src\gui_app.py
echo.
echo Make sure to:
echo   1. Start Roblox first
echo   2. Then click START in the GUI
echo.
pause
