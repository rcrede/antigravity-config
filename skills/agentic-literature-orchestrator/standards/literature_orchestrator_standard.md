---
date created: 2026-07-09T18:56:10+02:00
date modified: 2026-07-15T20:23:45+02:00
---

## Agentic Literature Orchestrator Standard

NaN) **Strict Halting:** The orchestrator MUST pause execution after Phase 2 (Dual-Sided Condensation). It must yield control to the user so they can review the newly generated Zettels.

NaN) **Resumption Protocol:** The orchestrator may only proceed to Phase 3 (SOTA Synthesis) once the user has explicitly confirmed the review IS COMPLETE AND a programmatic verification check via the Obsidian CLI (e.g., `obsidian search query="#zettel/unreviewed" path="40_Zettelkasten" total`) confirms 0 instances of the tag in the relevant scope.

NaN) **No Skipping:** The pipeline phases must be executed in sequence without bypassing the Rigor Review or Council constraints.
