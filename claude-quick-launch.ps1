#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Claude Code Quick Launcher - Paleisti LiteLLM agentus iš Claude

.DESCRIPTION
    Šis script'as paleidžia agentus tiesiogiai iš Claude Code terminal

.EXAMPLE
    .\claude-quick-launch.ps1
    .\claude-quick-launch.ps1 -Quick
    .\claude-quick-launch.ps1 -FullAgents
#>

param(
    [switch]$Quick,
    [switch]$FullAgents
)

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptPath

Write-Host "🚀 Claude Code Quick Launcher" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

if ($Quick -or -not $FullAgents) {
    Write-Host "⚡ Running quick test..." -ForegroundColor Green
    python quick-test.py
} else {
    Write-Host "🤖 Running full agents..." -ForegroundColor Green
    python claude_agent_example.py
}
