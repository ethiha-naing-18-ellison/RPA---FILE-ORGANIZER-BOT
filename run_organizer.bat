@echo off
REM File Organizer Bot - Windows Launcher
REM Double-click this file to start the File Organizer Bot

title File Organizer Bot

echo.
echo ================================
echo   File Organizer Bot
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if the main script exists
if not exist "file_organizer_bot.py" (
    echo ERROR: file_organizer_bot.py not found
    echo.
    echo Please make sure this batch file is in the same folder
    echo as the file_organizer_bot.py script.
    echo.
    pause
    exit /b 1
)

echo Starting File Organizer Bot...
echo.

REM Run the Python script
python file_organizer_bot.py

REM Check if there was an error
if errorlevel 1 (
    echo.
    echo The script encountered an error.
    echo.
    pause
    exit /b 1
)

echo.
echo File Organizer Bot finished successfully.
pause