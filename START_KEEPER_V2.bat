@echo off
REM Start Anime Vanguards Keeper V2 - Industry Grade Edition

title Anime Vanguards Keeper V2

cd /d "%~dp0"

echo ========================================
echo   ANIME VANGUARDS KEEPER V2
echo   Industry-Grade Edition
echo ========================================
echo.
echo Features:
echo   - Multi-method click system (4 fallback methods)
echo   - PyDirectInput for better game recognition
echo   - PostMessage for fastest background clicks
echo   - Humanization to avoid detection
echo   - Enhanced error handling
echo.
echo Make sure:
echo   1. Roblox is running
echo   2. You are in Anime Vanguards
echo   3. You are in AFK chamber
echo.
pause

echo.
echo Starting Keeper V2...
py src\gui_app_v2.py

pause
