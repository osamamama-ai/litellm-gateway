@echo off
chcp 65001 >nul
title LiteLLM Proxy

echo.
echo Paleidžiu LiteLLM proxy (127.0.0.1:4000)...
echo.
echo Šį langą laikyk atidarytą!
echo Norėdamas sustabdyti: Ctrl+C
echo.

litellm --config_dir . --port 4000
