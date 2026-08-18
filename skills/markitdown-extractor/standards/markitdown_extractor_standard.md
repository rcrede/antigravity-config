---
date created: 2026-07-09T18:54:11+02:00
date modified: 2026-07-15T20:23:43+02:00
---

## MarkItDown Extractor Standard

NaN) **Self-Contained Extraction:** The agent must ALWAYS use the `scripts/extract.sh` script to perform extraction via Pixi, rather than calling `uvx markitdown` or `pip install` directly.

NaN) **Output Formatting:** The output should be placed in the `50_Literature/raw/` directory unless otherwise specified by the orchestrator.

NaN) **No Mutilation:** The extracted text must be kept entirely raw. Do not attempt to summarize or shorten the output of the extraction script.
