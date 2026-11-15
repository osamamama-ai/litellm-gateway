@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
title LiteLLM - Paprasta pradzia

:menu
cls
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║          LiteLLM - Paprasta pradzia               ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo Pasirink ka nori:
echo.
echo   1 - Pradeti PROXY (reikalingas pirmas)
echo   2 - Pradeti Claude Code (su cheap-code)
echo   3 - Pradeti Claude Code (su haiku - pigiausias Claude)
echo   4 - Pradeti Claude Code (su deepseek - pigiausias)
echo   5 - Pradeti abi (proxy + cheap-code)
echo.
echo   0 - Iseiti
echo.
set /p choice="Pasirink (0-5): "

if "%choice%"=="1" goto :proxy
if "%choice%"=="2" goto :claude_cheap
if "%choice%"=="3" goto :claude_haiku
if "%choice%"=="4" goto :claude_deep
if "%choice%"=="5" goto :both
if "%choice%"=="0" exit /b
echo Neteisingas pasirinkimas!
timeout /t 2 >nul
goto :menu

:proxy
echo.
echo Paleidziu proxy... (127.0.0.1:4000)
echo Neuzdaryk sito lango!
echo.
cd /d C:\Users\osama\litellm-gateway
powershell -NoProfile -ExecutionPolicy Bypass -File "start-proxy.ps1"
goto :menu

:claude_cheap
echo.
echo Paleidziu Claude Code su cheap-code...
echo.
call claude-llm.cmd --model cheap-code
echo.
pause
goto :menu

:claude_haiku
echo.
echo Paleidziu Claude Code su haiku (pigiausias Claude)...
echo.
call claude-llm.cmd --model claude-haiku-5-5
echo.
pause
goto :menu

:claude_deep
echo.
echo Paleidziu Claude Code su deepseek-flash (pigiausias)...
echo.
call claude-llm.cmd --model deepseek-flash
echo.
pause
goto :menu

:both
echo.
echo Paleidziu PROXY naujame lange...
start "LiteLLM Proxy" powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\osama\litellm-gateway\start-proxy.ps1"
timeout /t 3 >nul
echo.
echo Paleidziu Claude Code su cheap-code...
call claude-llm.cmd --model cheap-code
goto :menu
