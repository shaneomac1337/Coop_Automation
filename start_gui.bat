@echo off
REM Launcher for Coop Store Configuration Generator GUI
REM Double-click this file to start the application

echo Starting Coop Store Configuration Generator...
echo.

python src\gui.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start the application.
    echo Please make sure Python is installed and in your PATH.
    echo.
    pause
)
