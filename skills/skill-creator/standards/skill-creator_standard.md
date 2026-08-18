---
date created: 2026-07-16T19:40:00+02:00
---

# Skill Creator Standard

This file dictates the execution constraints for the `skill-creator` skill.

**1. Never skip the Reflect-Extract-Inject loop:** The agent must never manually write the final skill without first testing it against the "Train" set and reflecting on the trace execution.
**2. Always enforce the Standards directory:** The agent must always create a `standards/` directory for any new skill and symlink the resulting standard `.md` file to `80_System/Standards/`.
**3. Must route complexity:** For complex skills, the agent must decompose the logic into a deterministic multi-agent DAG or Python orchestrator, rather than a monolithic prompt.
**4. Always split test cases:** The agent must separate user test cases into a "Train" set for iteration and a "Validation" set for the final executive summary.
