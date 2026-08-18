---
date created: 2026-07-09T18:54:51+02:00
date modified: 2026-07-09T23:59:03+02:00
---

## Dual-Sided Compiler Standard

NaN) **Self-Contained Scaffolding:** The agent must ALWAYS use the `scripts/scaffold_dsln.py` script to generate the markdown files and write the YAML frontmatter. Do not write the files manually via `write_to_file`.

NaN) **Post-Scaffold Drafting:** After the script runs, the agent must use `replace_file_content` to fill in the "dense summary" placeholder inside the DSLN file based on its reading of the raw markdown.

NaN) **Zettel Tagging:** The scaffolding script automatically tags new Zettels with `#zettel/unreviewed`. The agent must NOT remove this tag.
