@echo off
title Education Gap AI Agent Web Portal
echo ======================================================
echo       Education Gap AI Agent Web Application
echo ======================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to your system PATH.
    echo Please install Python 3.8+ to run the local server.
    echo.
    pause
    exit /b 1
)

echo Initializing local HTTP server and launching web portal...
echo.
python server.py

echo.
echo ======================================================
echo Web server terminated.
pause
