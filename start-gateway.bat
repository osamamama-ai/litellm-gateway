@echo off
REM LiteLLM Gateway - Easy Start for Windows
REM Simply double-click this file to start the gateway!

echo.
echo =====================================
echo  LiteLLM Gateway Startup
echo =====================================
echo.

REM Load environment variables from .env file
if exist .env (
    for /f "delims== tokens=1,2" %%a in (.env) do set %%a=%%b
)

if "%OPENROUTER_API_KEY%"=="" (
    echo ERROR: OPENROUTER_API_KEY not set. Create .env file with your keys.
    pause
    exit /b 1
)

echo Gateway starting...
echo.
echo Gateway URL:    http://127.0.0.1:4000
echo Master Key:     sk-gateway-...
echo.
echo Available Models:
echo   - deepseek-flash    ($0.014/1M tokens)
echo   - deepseek-pro      ($0.27/1M tokens)
echo   - claude-haiku-5-5  ($0.08/1M tokens)
echo   - cheap-code        ($0.05/1M tokens)
echo   - claude-sonnet-5   ($3.00/1M tokens)
echo.
echo Usage: python gateway_client.py
echo.

litellm_proxy --config config.yaml

pause
