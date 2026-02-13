$gitPath = (Get-Command git.exe -ErrorAction SilentlyContinue).Source
if (-not $gitPath) {
    if (Test-Path "C:\Program Files\Git\cmd\git.exe") { $gitPath = "C:\Program Files\Git\cmd\git.exe" }
    elseif (Test-Path "C:\Program Files (x86)\Git\cmd\git.exe") { $gitPath = "C:\Program Files (x86)\Git\cmd\git.exe" }
}

if ($gitPath) {
    Write-Host "🔄 Creating lightweight price data for cloud..." -ForegroundColor Cyan
    python create_light_data.py
    
    Write-Host "📦 Staging files..." -ForegroundColor Cyan
    & $gitPath add us_daily_prices_light.csv
    & $gitPath add -f *.json
    & $gitPath add flask_app.py templates/index.html
    
    Write-Host "💾 Committing changes..." -ForegroundColor Cyan
    & $gitPath commit -m "Update market data and dashboard"
    
    Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Cyan
    & $gitPath push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ SUCCESS: Deployed to GitHub!" -ForegroundColor Green
        Write-Host "Render will auto-deploy in 2-3 minutes." -ForegroundColor Gray
    }
    else {
        Write-Host "`n❌ FAILED: Please check for errors above." -ForegroundColor Red
    }
}
else {
    Write-Host "Git not found! Please install Git for Windows." -ForegroundColor Red
}

Read-Host -Prompt "Press Enter to exit"
