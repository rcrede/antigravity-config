---
name: session-wrap-up
description: Vault Housekeeper and Meta-Learner. Triggers at the end of a session to consolidate knowledge, update active project state, update global AI preferences/standards, atomize notes to Zettels, create transcluded atomic logs, and execute a state-saving git commit.
---

# Session Wrap-up (Vault Housekeeper)

This skill executes a complete state-saving and meta-learning routine at the end of an AI working session.

## Triggers
- When the user explicitly asks to "wrap up the session", "finish for today", or "run the wrap-up skill".

## Execution

**Crucial Constraint:** You must use the `session_wrap_up_referee.py` script to manage the state of the wrap-up. The script will tell you exactly what to do at each phase. You CANNOT advance until the script permits it. Furthermore, you must strictly obey any `MANDATORY TOOL CONSTRAINT` printed by the script; if it forbids certain tools, do not use them.

1. **Initialization:** Run the script to start the wrap-up.
   ```bash
   cd /home/rcrede/.gemini/config/skills/session-wrap-up/scripts
   pixi run python session_wrap_up_referee.py init
   ```
2. **Follow Instructions:** The script will output `STATE`, `ACTION`, and `MANDATORY TOOL CONSTRAINT`. **Follow them exactly**.
3. **Advance:** When you complete a phase, advance to the next one:
   ```bash
   pixi run python session_wrap_up_referee.py advance --to HOUSEKEEPING
   ```
   (Valid targets: `HOUSEKEEPING`, `PROJECT_STATE`, `LOGGING`, `COMPLETED`)
