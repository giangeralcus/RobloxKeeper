@echo off
REM Anime Vanguards Keeper - Launcher
REM Windows Edition

title Anime Vanguards Keeper

cd /d "%~dp0"

echo ========================================
echo   ANIME VANGUARDS KEEPER
echo ========================================
echo.
echo Starting GUI application...
echo.

python src\gui_app.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to start the application!
    echo.
    echo Please make sure:
    echo   1. Python is installed
    echo   2. You ran "install.bat" first
    echo   3. All dependencies are installed
    echo.
    pause
)
