@echo off
REM LiteLLM Gateway - EASY START FOR WINDOWS
REM Just double-click this file!

echo.
echo =====================================
echo   LiteLLM Gateway - 5 AI Models
echo =====================================
echo.

cd /d C:\Users\osama\litellm-gateway

REM Load environment variables from .env file if it exists
if exist .env (
    for /f "delims== tokens=1,2" %%a in (.env) do set %%a=%%b
)

REM Verify required keys are set
if "%OPENROUTER_API_KEY%"=="" (
    echo ERROR: OPENROUTER_API_KEY not set in .env file
    echo Create .env file with your keys (see .env.example)
    pause
    exit /b 1
)

echo.
echo Gateway starting on: http://127.0.0.1:4000
echo.
echo Available Models:
echo   deepseek-flash    - $0.014/1M tokens (CHEAPEST)
echo   deepseek-pro      - $0.27/1M tokens
echo   claude-haiku-5-5  - $0.08/1M tokens
echo   cheap-code        - $0.05/1M tokens
echo   claude-sonnet-5   - $3.00/1M tokens (backup)
echo.
echo Usage from another terminal:
echo   python gateway_client.py
echo.
echo Press Ctrl+C to stop.
echo =====================================
echo.

python -m litellm.proxy --config config.yaml

pause
