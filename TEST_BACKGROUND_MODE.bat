@echo off
REM Quick test for Windows API background mode
REM Based on MyBot-MBR analysis

title Test Background Mode - RobloxKeeper

cd /d "%~dp0"

echo ========================================
echo   BACKGROUND MODE TEST
echo ========================================
echo.
echo This will test TRUE background operation
echo using Windows API (SendMessage + PrintWindow)
echo.
echo BEFORE YOU START:
echo 1. Make sure Roblox is RUNNING
echo 2. Join Anime Vanguards game
echo 3. Stay in AFK chamber
echo.
echo WHAT TO WATCH FOR:
echo - Does Roblox window flash? (It SHOULDN'T!)
echo - Does the click work? (Check if character moves)
echo - Can you keep working? (Try typing while test runs)
echo.
pause

echo.
echo Installing pywin32 (if not installed)...
py -m pip install pywin32 --quiet

echo.
echo Running background mode test...
echo.
py background_mode_prototype.py

echo.
echo ========================================
echo   TEST COMPLETE
echo ========================================
echo.
echo Check the results above!
echo.
echo If you saw NO window flash:
echo   ^> SUCCESS! Windows API works!
echo.
echo If screenshot was captured:
echo   ^> Check: test_screenshot_background.png
echo.
echo If Roblox responded to click:
echo   ^> Ready to integrate into keeper!
echo.
pause
