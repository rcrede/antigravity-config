---
name: MapWeaver
description: >
  Lightweight YAML-frontmatter Obsidian Vault indexer. Use this skill when you need to regenerate the structure of a Zettelkasten or Obsidian Vault. It extracts frontmatter metadata (type, description/summary, status, tags, aliases) with zero LLM overhead.
---
# MapWeaver

MapWeaver is a lightweight YAML-frontmatter Obsidian Vault indexer. It replaces the old, deprecated AST-parsing tool with a zero-LLM overhead, YAML-driven structural indexer designed specifically for a 3-tier Zettelkasten layout.

## Deprecation Notice
**The old AST-based python codebase parser has been completely deprecated.** MapWeaver is no longer used for code symbol extraction, AST line mapping, or query-based semantic searches of code files. Do not attempt to use the `--query` flag or expect AST metadata.

## How to use MapWeaver

MapWeaver provides a single script to rebuild the vault index hierarchy at `scripts/mapweaver.py`.

### Generating or Updating the Map

When you need to index a vault or update existing index files:
```bash
python /home/rcrede/.gemini/config/skills/mapweaver/scripts/mapweaver.py --build <target-directory>
```

**Functionality:**
1. **Root `.CODEMAP.md`:** MapWeaver will generate exactly ONE `.CODEMAP.md` at the root of the target directory. This file maps the top-level directories of the vault.
2. **Top-Level `_Index.md`:** MapWeaver will generate exactly ONE `_Index.md` inside each top-level directory. This file recursively lists all markdown files within that directory along with their extracted YAML frontmatter.
3. **Extracted Metadata:** It parses `.md` files to extract ONLY these YAML keys: `type`, `description` (or `summary`), `status`, `tags`, and `aliases`.
4. **No LLM Overhead:** The script runs entirely deterministically and does not require the agent to read source files or replace TODO placeholders.

**Always run this tool after performing large structural changes to the Obsidian Vault** to ensure the navigation layer is up to date with the latest frontmatter changes.
