---
name: session-briefing
description: Context Bootstrapper. Triggers at the start of a new session to seamlessly resume work by identifying manual human edits via git diffs and retrieving active project state.
---

# Session Briefing (Context Bootstrapper)

This skill executes at the beginning of a new AI working session to rapidly bring the agent up to speed on what the user has done manually and where the project currently stands.

## Triggers
- When the user says "brief me", "start a new session", or asks "where were we?"

## Execution

**Crucial Constraint:** You must use the `session_briefing_referee.py` script to manage the state of the briefing. The script will tell you exactly what to do at each phase. You CANNOT advance until the script permits it. Furthermore, you must strictly obey any `MANDATORY TOOL CONSTRAINT` printed by the script; if it forbids certain tools, do not use them.

1. **Initialization:** Run the script to start the briefing.
   ```bash
   cd /home/rcrede/.gemini/config/skills/session-briefing/scripts
   pixi run python session_briefing_referee.py init --workspace "/home/rcrede/.gemini/antigravity/worktrees/Obsidian Vault/daily-briefing-leftover-tasks"
   ```
2. **Follow Instructions:** The script will output `STATE`, `ACTION`, and `MANDATORY TOOL CONSTRAINT`. **Follow them exactly**.
3. **Submit Diff:**
   ```bash
   pixi run python session_briefing_referee.py submit_diff --output "..."
   ```
4. **Submit Project State:**
   ```bash
   pixi run python session_briefing_referee.py submit_project_state --state "..."
   ```
5. **Complete:** Once synthesized, run:
   ```bash
   pixi run python session_briefing_referee.py complete
   ```
