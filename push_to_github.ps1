$gitPath = (Get-Command git.exe -ErrorAction SilentlyContinue).Source
if (-not $gitPath) {
    if (Test-Path "C:\Program Files\Git\cmd\git.exe") { $gitPath = "C:\Program Files\Git\cmd\git.exe" }
    elseif (Test-Path "C:\Program Files (x86)\Git\cmd\git.exe") { $gitPath = "C:\Program Files (x86)\Git\cmd\git.exe" }
}

if ($gitPath) {
    Write-Host "Git found at: $gitPath"
    & $gitPath push -u origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nSUCCESS: Pushed to GitHub!" -ForegroundColor Green
    } else {
        Write-Host "`nFAILED: Please check if a login window opened in the background." -ForegroundColor Red
    }
} else {
    Write-Host "Git not found! Please install Git for Windows." -ForegroundColor Red
}
