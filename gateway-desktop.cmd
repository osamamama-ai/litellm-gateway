@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python nėra įdiegtas!
    echo Atsisiusk iš: https://python.org
    pause
    exit /b 1
)

REM Check if PyQt6 is installed
python -c "import PyQt6" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⏳ Diegiu PyQt6...
    python -m pip install -q PyQt6
)

REM Run the app
echo ✅ Paleidžiama Desktop App...
python "%~dp0gateway-desktop.py"
