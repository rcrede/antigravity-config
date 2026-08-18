#!/usr/bin/env bash
set -e

sync_repo() {
  local dir="$1"
  local name="$2"
  echo "🔄 Syncing ${name}..."
  cd "${dir}"
  if [[ -n $(git status -s) ]]; then
    git add .
    git commit -m "sync: ${name} update $(date +'%Y-%m-%d %H:%M')"
  fi
  git pull --rebase origin main || true
  git push origin main
}

sync_repo "${HOME}/.gemini/config" "Antigravity Config"
sync_repo "${HOME}/Documents/Obsidian Vault" "Obsidian Vault"

echo "✅ All Second Brain systems synchronized with GitHub!"
