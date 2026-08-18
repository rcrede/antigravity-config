Write-Host "🔄 [1/2] Syncing Antigravity Config..." -ForegroundColor Cyan
Set-Location "$HOME\.gemini\config"
git pull --rebase origin main
if (git status -s) {
    git add .
    git commit -m "sync: antigravity config update $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git push origin main
}

Write-Host "🔄 [2/2] Syncing Obsidian Vault..." -ForegroundColor Cyan
Set-Location "$HOME\Documents\Obsidian Vault"
git pull --rebase origin main
if (git status -s) {
    git add .
    git commit -m "sync: vault update $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git push origin main
}

Write-Host "✅ All Second Brain systems synchronized with GitHub!" -ForegroundColor Green
