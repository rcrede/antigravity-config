---
date created: 2026-07-16T19:40:00+02:00
---

# Standards Writer Standard

This file dictates the execution constraints for the `standards-writer` skill.

**1. Never skip the Meta-Standard check:** The agent must never create or refactor a standard without first reading `80_System/Standards/standards_meta_standard.md`.
**2. Always use absolute language:** The agent must use deterministic language ("must", "never", "always") and avoid soft suggestions ("should", "might").
**3. Must employ Constraint-First Structure:** The agent must place destructive prevention rules (what NOT to do) as the very first rule in the standard.
**4. Always number and bold rules:** The agent must format all rules with bold numbering and provide a brief contextual explanation for why the rule exists.
