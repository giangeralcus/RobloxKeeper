@echo off
REM Coordinate Calibration Tool

title Coordinate Calibration

cd /d "%~dp0"

echo ========================================
echo   COORDINATE CALIBRATION TOOL
echo ========================================
echo.
echo This tool will help you set exact click positions
echo for your Roblox window size.
echo.
echo BEFORE YOU START:
echo 1. Start Roblox
echo 2. Go to Roblox HOME page
echo 3. Make sure you can see Anime Vanguards game
echo.
pause

py src\calibrate_coordinates.py

pause
