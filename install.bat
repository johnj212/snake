@echo off
echo ===============================================
echo    Python Snake Game - Installation Script
echo         Play Against the Computer!
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.x from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python detected:
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed with Python
    echo.
    pause
    exit /b 1
)

echo Installing required packages...
echo.

REM Install pygame
echo Installing pygame...
pip install pygame==2.5.2
if %errorlevel% neq 0 (
    echo WARNING: Failed to install specific pygame version, trying latest...
    pip install pygame
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install pygame
        echo Please check your internet connection and try again
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ===============================================
echo          Installation Complete!
echo ===============================================
echo.
echo The Snake game is now ready to play!
echo.
echo To start the game, run:
echo   python main.py
echo.
echo Game Features:
echo   - Single Player: Classic Snake gameplay
echo   - AI Mode: Play against 3 computer opponents
echo   - Balanced gameplay with strategic advantages
echo.
echo Controls:
echo   - Menu: Press 1 for Single Player, 2 for AI Mode
echo   - Game: Use arrow keys to control your snake
echo   - ESC: Return to menu anytime
echo.
echo Have fun playing Snake!
echo.
pause
