$ErrorActionPreference = "Stop"
$root = "C:\Users\efeka\Hayvan-Kanali"
$python = "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\python3.12.exe"
# @main jsDelivr cache'i icerik degistiginde saatlerce bayat kalabiliyor;
# commit hash'e sabitlemek her push sonrasi anlik guncel dosya garantisi verir.
# Yeni video/muzik/caption pushlandiginda bu hash'i `git rev-parse HEAD` ile guncelle.
$template = "https://cdn.jsdelivr.net/gh/mehmetceylann42-gif/pati-sifresi-reels@d8cef1e5e3d840f9293d67f797fd008dde3bbcf8/videos/{slug}.mp4"
$logDir = Join-Path $root "logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$logFile = Join-Path $logDir ("publish_{0}.log" -f (Get-Date -Format "yyyy-MM-dd_HHmmss"))

Set-Location $root
& $python "scripts\publish_queue.py" --video-url-template $template --publish --limit 1 *>> $logFile
