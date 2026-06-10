# ============================================================
# Start Backend + Frontend (Robust Windows version)
# ============================================================

Write-Host "🎵 Starting Music Player..." -ForegroundColor Cyan
Write-Host ""

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

$backendPath  = Join-Path $projectRoot "Backend"
$pythonExe    = Join-Path $projectRoot ".venv\Scripts\python.exe"
$frontendPath = Join-Path $projectRoot "Frontend"

# --- Basic checks ---
if (-not (Test-Path $pythonExe)) {
    Write-Host "❌ ERROR: Python venv not found!" -ForegroundColor Red
    Write-Host "   Expected at: $pythonExe" -ForegroundColor Yellow
    exit 1
}

# Try to find npm
$npmCmd = Get-Command npm -ErrorAction SilentlyContinue
if (-not $npmCmd) {
    Write-Host "❌ ERROR: 'npm' command not found in PATH." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Found npm at: $($npmCmd.Source)" -ForegroundColor Green

# ============================================================
# Start Backend in new window
# ============================================================
Write-Host "🚀 Launching Backend in new window..." -ForegroundColor Cyan

Start-Process -WorkingDirectory $backendPath `
              -FilePath $pythonExe `
              -ArgumentList "main.py" `
              -WindowStyle Normal

Start-Sleep -Seconds 2

# ============================================================
# Start Frontend using cmd.exe (most reliable method)
# ============================================================
Write-Host "🚀 Launching Frontend in new window..." -ForegroundColor Cyan

$frontendCmd = "cd /d `"$frontendPath`" && npm run dev"
Start-Process -FilePath "cmd.exe" `
              -ArgumentList "/k", $frontendCmd `
              -WindowStyle Normal

# ============================================================
# Finished
# ============================================================
Write-Host ""
Write-Host "✅ Backend should be at:  http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "✅ Frontend should be at: http://localhost:5173" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Close the two black terminal windows to stop the services." -ForegroundColor Yellow
Write-Host ""