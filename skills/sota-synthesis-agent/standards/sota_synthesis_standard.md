---
date created: 2026-07-09T18:55:34+02:00
date modified: 2026-07-15T20:23:41+02:00
---

## SOTA Synthesis Standard

NaN) **Self-Contained Traversal:** The agent must ALWAYS use the `scripts/extract_graph.py` script to deterministically extract the scoped sub-graph of DSLNs and reviewed Zettels. Do not try to manually `grep` or use `obsidian-cli` to find files, as the script handles filtering out unreviewed notes automatically.

NaN) **Output Formatting:** The output must be written to `State_Of_The_Art_Report.md`.

NaN) **No Hallucination:** Ensure all contradictions and gaps are strictly derived from the extracted graph JSON, with citations back to the source DSLNs.
