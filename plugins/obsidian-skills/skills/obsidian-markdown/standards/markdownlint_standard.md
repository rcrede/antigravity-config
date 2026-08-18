---
name: markdownlint-standard
description: >-
  Strictly enforces standard markdownlint rules across all markdown files generated or edited by the agent.
  Use whenever generating documentation, creating READMEs, or modifying AGENTS.md files.
date created: 2026-06-18T22:46:59+02:00
date modified: 2026-07-09T23:59:05+02:00
---

## Markdownlint Standard

To ensure that machine-to-machine (M2M) documentation and human documentation render perfectly and are easily parsed by linters, all markdown files must strictly adhere to the following rules:

### 1. Heading Formatting

- **MD001 (Heading Increment):** Headings must increment by one level at a time (e.g., `#` followed by `##`, not `###`).
- **MD002 (First Heading):** The first heading in the document must be a top-level heading (`#`).
- **MD003 (Heading Style):** Always use ATX-style headings (e.g., `## Heading`). Never use Setext style (underlining with `===` or `---`).
- **MD022 (Heading Blank Lines):** Headings must be surrounded by blank lines.

### 2. Lists

- **MD004 (Unordered List Style):** Be consistent. Prefer asterisks `*` or hyphens `-` for bullet points, but do not mix them in the same file.
- **MD005 (Inconsistent Indentation):** Sub-lists must be indented exactly 2 or 4 spaces consistently.
- **MD007 (Unordered List Indentation):** Unordered lists should be indented by 2 spaces per level.
- **MD032 (List Blank Lines):** Lists must be surrounded by blank lines to prevent them from merging with surrounding text.

### 3. Whitespace & Lines

- **MD009 (Trailing Spaces):** No trailing spaces are permitted at the end of lines.
- **MD010 (Hard Tabs):** Never use hard tabs; use spaces for indentation.
- **MD012 (Multiple Blank Lines):** Do not use consecutive blank lines. One blank line is sufficient to separate blocks.
- **MD047 (Single Trailing Newline):** Files must end with a single newline character.

### 4. Code Blocks

- **MD031 (Fenced Code Blocks):** Fenced code blocks must be surrounded by blank lines.
- **MD040 (Fenced Code Language):** Fenced code blocks must have a specified language (e.g., `python`, `bash`, `text`).

### 5. Automated Formatting (Obsidian Linter)

To ensure total compliance without manual pixel-pushing, you MUST utilize the native Obsidian Linter plugin via the `obsidian` CLI to automatically format all markdown files located inside the Obsidian vault.

- **Action:** When you finish writing or editing a `.md` file in this vault, you MUST run the linter on it to automatically fix trailing whitespaces, heading styles, properties, and missing newlines.
- **Command:** `obsidian eval code="app.commands.executeCommandById('obsidian-linter:lint-file')"` (Note: This lints the active file. If you are not sure the file is active, you can optionally run `obsidian tab:open file="YourFile.md"` first).

### 6. Automated Formatting (Outside the Vault)

If you are editing `.md` files outside of the Obsidian Vault (e.g., standard coding projects, scratch directories), the Obsidian CLI cannot access them. Instead, you MUST use `mdformat`.

- **Action:** Execute `mdformat <file_path>` from the terminal to automatically format the markdown file using standard rules.
- *Note: `mdformat` is globally installed in the environment via Pixi.*

### Agent Action Required

Whenever you write to or create a `.md` file, you MUST run the obsidian linter command via the CLI to verify that your text conforms to these rules. If the user reports a markdownlint error, immediately cross-reference this skill and trigger the linter.
