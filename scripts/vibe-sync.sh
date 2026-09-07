#!/usr/bin/env bash
set -e

sync_repo() {
  local dir="$1"
  local name="$2"
  echo "🔄 Syncing ${name}..."
  cd "${dir}"
  if [[ -d ".git/rebase-merge" || -d ".git/rebase-apply" ]]; then
    echo "⚠️ Ongoing rebase found in ${name}, aborting and resetting to remote..."
    git rebase --abort || true
    git fetch origin main
    git reset --hard origin/main
  fi

  if [[ -n $(git status -s) ]]; then
    git add .
    git commit -m "sync: ${name} update $(date +'%Y-%m-%d %H:%M')"
  fi

  if ! git pull --rebase origin main; then
    echo "⚠️ Conflict detected in ${name}, overwriting local with remote..."
    git rebase --abort || true
    git fetch origin main
    git reset --hard origin/main
  fi

  git push origin main
}

sync_repo "${HOME}/.gemini/config" "Antigravity Config"
sync_repo "${HOME}/Documents/Obsidian Vault" "Obsidian Vault"

echo "✅ All Second Brain systems synchronized with GitHub!"
