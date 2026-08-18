---
date created: 2026-07-16T20:45:00+02:00
---

# Storm Council Standard

This standard dictates the execution constraints for the `storm-council` skill.

**1. Never prompt sequentially in Markdown:** The agent must never attempt to execute the multi-step Storm Council workflow directly in chat. LLMs are prone to skipping steps or hallucinating subagents during long sequential prompts.
**2. Always use the Pixi Orchestrator:** The agent must always trigger the `storm_orchestrator.py` script via `pixi run` to execute the council. The script handles the state machine, API calls, and JSON hooks deterministically.
**3. Must pass raw proposals directly:** The agent must pass the user's raw proposal or question exactly as written into the orchestrator script without attempting to pre-summarize it, to preserve the original stakes and context.
