$port = 9999
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)

$ips = Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
    $_.IPAddress -notlike "127.*" -and $_.InterfaceAlias -notlike "*Loopback*"
} | Select-Object -ExpandProperty IPAddress

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Aliyun ACP Docs Server" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Docs: bei kao wen dang (6 parts / 132 docs)" -ForegroundColor Gray
Write-Host ""

foreach ($ip in $ips) {
    Write-Host "  LAN : http://${ip}:${port}" -ForegroundColor Green
}
Write-Host "  Local: http://localhost:${port}" -ForegroundColor Green
Write-Host ""
Write-Host "  Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

Start-Process "http://localhost:${port}"
python -X utf8 doc_server.py
