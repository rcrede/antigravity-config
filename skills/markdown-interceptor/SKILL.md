---
name: markdown-interceptor
description: >-
  FATAL INTERCEPTOR: Do NOT create or edit any .md file in an Obsidian vault before reading this. 
  This skill intercepts all attempts to write or edit markdown files to enforce the post-edit Linter step.
---

# Markdown Editor Interceptor

**STOP.** If you are about to edit or create a `.md` file, you must adhere strictly to the following rules based on the file's location. 

## 1. Context Check (Vault vs Scratch)

First, determine if the target `.md` file is located inside the user's Obsidian Vault (e.g., `/home/rcrede/Documents/Obsidian Vault/`).
- **If OUTSIDE the Vault (e.g., in a scratch directory):** The Obsidian CLI cannot access it. Instead, you **MUST** run `mdformat <file_path>` via the terminal to format the file after editing.
- **If INSIDE the Vault:** You **MUST** trigger the Obsidian Linter immediately after editing to ensure compliance with the `markdownlint_standard`. Follow the rules below based on your execution method.

## 2. Vault Execution Rules

Depending on how you edit the file in the vault, you must enforce the Linter post-edit.

### Case A: Native Agent Tools (replace_file_content / write_to_file)
When you use your native tools to edit the file, the file is modified on disk but Obsidian's UI might not format it automatically. 
**Mandatory Post-Edit Action:** You must run the following bash command to open the file in the Obsidian UI and trigger the Linter:
```bash
obsidian tab:open file="<FileName.md>" && sleep 1 && obsidian eval code="app.commands.executeCommandById('obsidian-linter:lint-file')"
```

### Case B: Scripted Pipelines (Python/Bash)
If you write a script to bulk-generate or edit files (e.g., generating Zettels):
**Mandatory Action:** The script must conclude by either invoking the `obsidian eval` linter command on the generated files via `subprocess.run()`, or you as the agent must manually sweep and lint the files using the CLI after the script finishes.

### Case C: CLI Direct Commands (obsidian create / append)
If you use the `obsidian-cli` to create or append to files directly.
**Mandatory Action:** The CLI does not automatically lint upon creation. You must follow up with the same linter eval command shown in Case A.

## Agent Directive
Do not skip the linting step. The vault must remain perfectly formatted for machine parsability at all times.
