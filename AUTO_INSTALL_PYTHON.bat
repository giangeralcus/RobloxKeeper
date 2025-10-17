@echo off
REM Auto-Install Python using Windows Package Manager
REM Run this as Administrator

echo ========================================
echo   AUTO PYTHON INSTALLER
echo ========================================
echo.

REM Check if winget is available
winget --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Windows Package Manager (winget) not found!
    echo.
    echo Please install Python manually from Microsoft Store:
    echo 1. Press Windows Key
    echo 2. Open "Microsoft Store"
    echo 3. Search "Python 3.12"
    echo 4. Click "Install"
    echo.
    pause
    exit /b 1
)

echo [OK] Windows Package Manager found
echo.

REM Install Python
echo Installing Python 3.12...
echo.
winget install Python.Python.3.12 --silent

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed!
    echo.
    echo Try manual installation:
    echo - Open Microsoft Store
    echo - Search "Python 3.12"
    echo - Click Install
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   PYTHON INSTALLED SUCCESSFULLY!
echo ========================================
echo.
echo Please CLOSE this window and open a NEW Command Prompt
echo Then run: python --version
echo.
echo After verifying Python works, run: install.bat
echo.
pause
