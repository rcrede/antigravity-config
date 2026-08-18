---
name: autonomous-research-pipeline
description: >-
  Master pipeline for end-to-end autonomous scientific research. Orchestrates Pixi environment setup, simulation scripting, the Marimo visualization pattern, explicit MapWeaver and Git housekeeping, ARA (Agent-Native Research Artifact) generation via the research-manager, and final paper compilation via paper-orchestra. Use this whenever instructed to run an autonomous research workflow or end-to-end simulation test.
---

# Autonomous Research Pipeline

## Overview
This skill codifies the complete, self-healing end-to-end autonomous research workflow. It bridges the gap between raw computational execution (simulations, data processing) and knowledge dissemination (paper generation). It relies heavily on explicit dependency checks and deterministic environmental hooks to ensure total success across subagent environments.

## Dependencies
- `pixi-orchestration`: For deterministic environment setup and task running.
- `MapWeaver`: For building `CODEMAP.md` indexes to manage agent context.
- `research-manager`: For explicitly compiling logical traces into the `ara/` workspace.
- `paper-orchestra`: For drafting and compiling the final LaTeX/Typst paper.

## Quick Start
When prompted to run the research pipeline, strictly follow the workflow below. Do not skip any explicit housekeeping or handoff steps.

## Execution

**Crucial Constraint:** You must use the `autonomous_research_referee.py` script to manage the state of the workflow. The script will tell you exactly what to do at each phase. You CANNOT advance until the script permits it. Furthermore, you must strictly obey any `MANDATORY TOOL CONSTRAINT` printed by the script; if it forbids certain tools, do not use them.

1. **Initialization:** Run the script to start the pipeline.
   ```bash
   cd /home/rcrede/.gemini/config/skills/autonomous-research-pipeline/scripts
   pixi run python autonomous_research_referee.py init
   ```
2. **Follow Instructions:** The script will output `STATE`, `ACTION`, and `MANDATORY TOOL CONSTRAINT`. **Follow them exactly**.
3. **Advance:** When you complete a phase, advance to the next one:
   ```bash
   pixi run python autonomous_research_referee.py advance --to MARIMO
   ```
   (Valid targets: `MARIMO`, `HOUSEKEEPING`, `ARA_HANDOFF`, `DISSEMINATION`, `COMPLETED`)

## Common Mistakes
- **Failing to Explicitly Run `research-manager`**: The biggest trap is forgetting Step 4. If `paper-orchestra` fails complaining about missing inputs, you skipped the explicit ARA handoff.
- **Mixing Logic and Presentation**: Do not write plotting logic in `01_scripts/`. Enforce the Marimo Pattern strictly.
- **Batching Commits**: Do not wait until the end to commit. Commit ultra-granularly after every script or plot creation.
