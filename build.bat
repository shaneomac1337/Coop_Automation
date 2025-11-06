@echo off
REM ============================================================
REM  Coop Store Configuration Generator
REM  Complete Build Script
REM ============================================================
REM
REM This script will:
REM 1. Create a fresh virtual environment
REM 2. Install all required dependencies
REM 3. Build the standalone executable
REM 4. Create distribution package
REM
REM Usage: Simply run this batch file
REM        build.bat
REM ============================================================

echo.
echo ============================================================
echo   Coop Store Configuration Generator - Build Script
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/5] Checking Python version...
python --version
echo.

REM Remove old build virtual environment if it exists
echo [2/5] Cleaning up old build environment...
if exist venv_build (
    echo   - Removing existing venv_build...
    rmdir /s /q venv_build
)
if exist build (
    echo   - Removing build artifacts...
    rmdir /s /q build
)
if exist dist (
    echo   - Removing old distribution...
    rmdir /s /q dist
)
if exist *.spec (
    echo   - Removing spec files...
    del /q *.spec
)
echo   Done!
echo.

REM Create fresh virtual environment
echo [3/5] Creating fresh virtual environment...
python -m venv venv_build
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo   Done!
echo.

REM Activate virtual environment and install dependencies
echo [4/5] Installing dependencies...
call venv_build\Scripts\activate.bat

echo   - Upgrading pip...
python -m pip install --upgrade pip --quiet

echo   - Installing pyinstaller...
pip install pyinstaller --quiet

echo   - Installing pandas...
pip install pandas --quiet

echo   - Installing openpyxl...
pip install openpyxl --quiet

echo   Done!
echo.

REM Build the executable
echo [5/5] Building executable...
echo   This may take a few minutes, please wait...
echo.
python scripts\build_exe.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    call venv_build\Scripts\deactivate.bat
    pause
    exit /b 1
)

REM Deactivate virtual environment
call venv_build\Scripts\deactivate.bat

echo.
echo ============================================================
echo   Build Complete! 
echo ============================================================
echo.
echo   Your executable is ready:
echo   Location: dist\CoopStoreConfig\CoopStoreConfig.exe
echo.
echo   Distribution package:
echo   Location: dist\CoopStoreConfig\
echo.
echo   To distribute:
echo   1. Zip the entire 'dist\CoopStoreConfig' folder
echo   2. Send to users
echo   3. Users unzip and run CoopStoreConfig.exe
echo.
echo   Cleaning up build environment...
echo   (Removing venv_build folder)
rmdir /s /q venv_build
echo.
echo   Done! You can close this window.
echo ============================================================
echo.
pause
