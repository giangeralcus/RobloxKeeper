@echo off
REM Install Tesseract OCR for text recognition

echo ========================================
echo   TESSERACT OCR INSTALLER
echo ========================================
echo.

echo Tesseract OCR is needed for text recognition.
echo.
echo OPTION 1: Download Installer (Recommended)
echo Opening download page...
echo.

start https://github.com/UB-Mannheim/tesseract/wiki

echo.
echo INSTRUCTIONS:
echo 1. Download "tesseract-ocr-w64-setup-5.3.x.exe"
echo 2. Run the installer
echo 3. During installation, note the install path
echo 4. Add to PATH or set TESSDATA_PREFIX environment variable
echo.
echo Default install path: C:\Program Files\Tesseract-OCR
echo.
echo After installation, the keeper will automatically use OCR
echo to find "ANIME VANGUARDS" game by reading text on screen!
echo.
pause
