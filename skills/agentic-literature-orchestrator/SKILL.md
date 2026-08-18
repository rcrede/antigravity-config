---
name: agentic-literature-orchestrator
description: Orchestrates the entire Agentic Literature Pipeline from PDF to ranked SOTA Gaps using the Cyborg Zettelkasten methodology.
---

# Agentic Literature Orchestrator

This master skill orchestrates the end-to-end literature review pipeline. It connects all sub-skills into a cohesive workflow with strict information provenance.
Before running, the agent must review the `standards/literature_orchestrator_standard.md` file for strict execution constraints (e.g. halting requirements).

## Execution

**Crucial Constraint:** You must use the `agentic_literature_referee.py` script to manage the state of the orchestrator. The script will tell you exactly what to do at each phase. You CANNOT advance until the script permits it. Furthermore, you must strictly obey any `MANDATORY TOOL CONSTRAINT` printed by the script; if it forbids certain tools, do not use them.

1. **Initialization:** Run the script to start the orchestrator.
   ```bash
   cd /home/rcrede/.gemini/config/skills/agentic-literature-orchestrator/scripts
   pixi run python agentic_literature_referee.py init
   ```
2. **Follow Instructions:** The script will output `STATE`, `ACTION`, and `MANDATORY TOOL CONSTRAINT` or `MANDATORY HALT`. **Follow them exactly**.
3. **Advance:** When you complete a phase, advance to the next one:
   ```bash
   pixi run python agentic_literature_referee.py advance --to CONDENSATION
   ```
   (Valid targets: `CONDENSATION`, `VERIFICATION`, `SYNTHESIS`, `RIGOR_COUNCIL`, `COMPLETED`)
