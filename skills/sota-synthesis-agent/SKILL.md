---
name: sota-synthesis-agent
description: Traverses Dual-Sided Literature Notes (DSLN) and reviewed Zettels to synthesize a State of the Art Report and identify gaps. Scopes traversal based on tags like #project or #topic.
---

# SOTA Synthesis Agent Skill

This skill acts as Step 3 in the Agentic Literature Pipeline. It aggregates claims from the Dual-Sided Literature Notes (DSLN) and verified Zettels to produce a `State_Of_The_Art_Report.md`.

## Execution

**Crucial Constraint:** You must use the `sota_synthesis_referee.py` script to manage the state of the synthesis. The script will tell you exactly what to do at each phase. You CANNOT advance until the script permits it. Furthermore, you must strictly obey any `MANDATORY TOOL CONSTRAINT` printed by the script; if it forbids certain tools, do not use them.

1. **Initialization:** Run the script to start the synthesis.
   ```bash
   cd /home/rcrede/.gemini/config/skills/sota-synthesis-agent/scripts
   pixi run python sota_synthesis_referee.py init --scope "#project/so3lr"
   ```
2. **Follow Instructions:** The script will output `STATE`, `ACTION`, and `MANDATORY TOOL CONSTRAINT`. **Follow them exactly**.
3. **Submit Graph Data:**
   ```bash
   pixi run python sota_synthesis_referee.py submit_graph --data "..."
   ```
4. **Advance:** When you complete a phase, advance to the next one:
   ```bash
   pixi run python sota_synthesis_referee.py advance --to REPORT
   ```
