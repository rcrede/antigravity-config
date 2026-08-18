function Sync-Repo {
    param([string]$Path, [string]$Name)
    Write-Host "🔄 Syncing $Name..." -ForegroundColor Cyan
    Set-Location $Path
    if (git status -s) {
        git add .
        git commit -m "sync: $Name update $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    }
    git pull --rebase origin main
    git push origin main
}

Sync-Repo "$HOME\.gemini\config" "Antigravity Config"
Sync-Repo "$HOME\Documents\Obsidian Vault" "Obsidian Vault"

Write-Host "✅ All Second Brain systems synchronized with GitHub!" -ForegroundColor Green
