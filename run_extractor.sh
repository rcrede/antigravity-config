#!/bin/bash
# run_extractor.sh — Stop hook handler for subagent log extraction
# Reads the event payload from stdin (JSON) and extracts subagent logs.
#
# The Stop event fires for BOTH the parent agent and subagents.
# We only want to extract logs for subagent conversations, not the parent.
# We detect this by checking if the conversationId differs from the
# current session's parent conversation ID.

STDIN_DATA=$(cat)

LOG="/home/rcrede/Documents/Obsidian Vault/10_Projects/hook_debug.log"

cd '/home/rcrede/Documents/Obsidian Vault' || exit 1

# Extract conversationId from the JSON payload
CONVERSATION_ID=$(python3 -c '
import sys, json
try:
    data = json.loads(sys.argv[1])
    print(data.get("conversationId", ""))
except Exception:
    print("")
' "$STDIN_DATA" 2>/dev/null)

if [ -z "$CONVERSATION_ID" ]; then
    exit 0
fi

# Check if transcript exists (subagents that ran will have one)
TRANSCRIPT="/home/rcrede/.gemini/antigravity/brain/${CONVERSATION_ID}/.system_generated/logs/transcript.jsonl"
if [ ! -f "$TRANSCRIPT" ]; then
    exit 0
fi

echo "[$(date -Iseconds)] Extracting logs for $CONVERSATION_ID" >> "$LOG"
pixi run python 80_System/Hooks/extract_subagent_logs.py "$CONVERSATION_ID" 10_Projects/Subagent_Execution_Logs.md >> "$LOG" 2>&1
