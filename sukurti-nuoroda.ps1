$desk = [Environment]::GetFolderPath('Desktop')
$gw   = 'C:\Users\osama\litellm-gateway'
$sh   = New-Object -ComObject WScript.Shell

$shortcut = $sh.CreateShortcut((Join-Path $desk 'LiteLLM - Paprasta.lnk'))
$shortcut.TargetPath       = "$env:WINDIR\System32\cmd.exe"
$shortcut.Arguments        = "/k `"$gw\paprasta-start.cmd`""
$shortcut.WorkingDirectory = $gw
$shortcut.Description      = 'LiteLLM - Paprasta pradžia (proxy + Claude Code)'
$shortcut.IconLocation     = "$env:WINDIR\System32\shell32.dll,109"
$shortcut.Save()

Write-Host "✅ Nuoroda 'LiteLLM - Paprasta' sukurta darbalaukyje!" -ForegroundColor Green
Write-Host ""
Write-Host "Dabar galite:" -ForegroundColor Cyan
Write-Host "1. Spustelti nuorodą darbalaukyje"
Write-Host "2. Pasirinkti 5 (pradėti abi)"
Write-Host "3. Darbas!"
