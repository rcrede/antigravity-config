---
name: standards-writer
description: Creates or refactors standards files in the vault to adhere to the global Standards Meta-Standard. Ensures all agentic constraints and formatting are deterministic and compliant.
---

# Standards Writer

This skill is used to write new standards or refactor existing ones, ensuring absolute conformity with the vault's central meta-standard.

## Triggers
- When the user asks to "write a standard for X", "refactor our standards", or "create a standard".
- When an agent realizes it is executing a repeated workflow that should be codified.

## Execution Steps

### 1. Read Meta-Standard
- **Strict Adherence:** Before writing, the agent MUST read `80_System/Standards/standards_meta_standard.md` using a file-reading tool.

### 2. Context Gathering
- **Read Existing:** If updating an existing standard, read it first.
- **Extract Preferences:** Read `80_System/Preferences.md` to ensure the new standard does not conflict with global user preferences.

### 3. Drafting the Standard
- **File Location:** Create or modify the standard in `80_System/Standards/[name]_standard.md`.
- **Constraint-First:** Ensure the first rule dictates what MUST NOT be done.
- **Formatting:** Use numbered lists with bold headers as mandated by the meta-standard. Use absolute language (must, never, always).

### 4. Verification
- Validate the newly written standard against the 5 rules in the meta-standard. If it fails any rule, revise it.
