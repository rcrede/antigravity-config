---
name: dual-sided-compiler
description: Converts Raw Markdown from literature into a Dual-Sided Literature Note (DSLN) and atomized Zettels. Integrates ara:compiler for extraction and ara:rigor-reviewer for claim validation.
---

# Dual-Sided Compiler Skill

This skill is Step 2 of the Agentic Literature Pipeline. It takes a Raw Markdown representation of a paper and transforms it into a Dual-Sided Literature Note (DSLN) and a set of atomized Zettelkasten notes.

## Execution

**Crucial Constraint:** You must use the `dual_sided_referee.py` script to manage the state. The script will tell you exactly what to do at each phase. You CANNOT advance until the script permits it. Furthermore, you must strictly obey any `MANDATORY TOOL CONSTRAINT` printed by the script; if it forbids certain tools, do not use them.

1. **Initialization:** Run the script to start the compilation.
   ```bash
   cd /home/rcrede/.gemini/config/skills/dual-sided-compiler/scripts
   pixi run python dual_sided_referee.py init
   ```
2. **Follow Instructions:** The script will output `STATE`, `ACTION`, and `MANDATORY TOOL CONSTRAINT`. **Follow them exactly**.
3. **Advance:** When you complete a phase, advance to the next one:
   ```bash
   pixi run python dual_sided_referee.py advance --to RIGOR_REVIEW
   ```
   (Valid targets: `RIGOR_REVIEW`, `SCAFFOLD`, `COMPLETED`)

## Output
- Return the absolute paths to the generated DSLN and the list of generated Zettels.
