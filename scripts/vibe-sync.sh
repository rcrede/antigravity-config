#!/usr/bin/env bash
set -e

echo "🔄 [1/2] Syncing Antigravity Config..."
cd "${HOME}/.gemini/config"
git pull --rebase origin main || true
if [[ -n $(git status -s) ]]; then
  git add .
  git commit -m "sync: antigravity config update $(date +'%Y-%m-%d %H:%M')"
  git push origin main
fi

echo "🔄 [2/2] Syncing Obsidian Vault..."
cd "${HOME}/Documents/Obsidian Vault"
git pull --rebase origin main || true
if [[ -n $(git status -s) ]]; then
  git add .
  git commit -m "sync: vault update $(date +'%Y-%m-%d %H:%M')"
  git push origin main
fi

echo "✅ All Second Brain systems synchronized with GitHub!"
