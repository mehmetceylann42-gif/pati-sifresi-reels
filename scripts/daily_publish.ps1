$ErrorActionPreference = "Stop"
$root = "C:\Users\efeka\Hayvan-Kanali"
$python = "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\python3.12.exe"
# @main jsDelivr cache'i icerik degistiginde saatlerce bayat kalabiliyor;
# commit hash'e sabitlemek her push sonrasi anlik guncel dosya garantisi verir.
# Yeni video/muzik/caption pushlandiginda bu hash'i `git rev-parse HEAD` ile guncelle.
$template = "https://cdn.jsdelivr.net/gh/mehmetceylann42-gif/pati-sifresi-reels@99e27271bd4bbab68f7d1f167fbac8934fa32303/videos/{slug}.mp4"
$logDir = Join-Path $root "logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$logFile = Join-Path $logDir ("publish_{0}.log" -f (Get-Date -Format "yyyy-MM-dd_HHmmss"))

Set-Location $root
& $python "scripts\publish_queue.py" --video-url-template $template --publish --limit 1 *>> $logFile
