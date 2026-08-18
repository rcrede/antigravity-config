---
name: skill-creator
description: Meta-skill to create, evaluate, and iteratively refine other agent skills using a Reflect-Extract-Inject loop and strict self-contained modularity.
---

# Agent Skill Creator

This skill orchestrates the end-to-end creation, evaluation, and refinement of AI agent skills. It utilizes a robust Reflect-Extract-Inject iteration loop and strictly enforces the user-defined Vault Modularity Standards.

## Execution

**Crucial Constraint:** You must use the `skill_creator_referee.py` script to manage the state of the creator. The script will tell you exactly what to do at each phase. You CANNOT advance until the script permits it. Furthermore, you must strictly obey any `MANDATORY TOOL CONSTRAINT` printed by the script; if it forbids certain tools, do not use them.

1. **Initialization:** Run the script to start the workflow.
   ```bash
   cd /home/rcrede/.gemini/config/skills/skill-creator/scripts
   pixi run python skill_creator_referee.py init
   ```
2. **Follow Instructions:** The script will output `STATE`, `ACTION`, and `MANDATORY TOOL CONSTRAINT`. **Follow them exactly**.
3. **Advance:** When you complete a phase, advance to the next one:
   ```bash
   pixi run python skill_creator_referee.py advance --to RESEARCH
   ```
   (Valid targets: `RESEARCH`, `DRAFTING`, `AUTOMATION_LOOP`, `BENCHMARK`, `COMPLETED`)

## Workflow
### 1. Capture Intent & Scaffolding
Start by understanding the user's intent. 
Ask clarifying questions to determine:
- What should this skill enable the agent to do?
- When should this skill trigger?
- What are the required test cases (inputs and expected outputs)? **Crucially, split these test cases into a "Train" set (used for iteration) and a hidden "Validation" set (used only for the final executive summary).**

### 2. Deep Research & Complexity Routing
Before drafting the skill, analyze its complexity.
- **Complexity Router:** If the skill requires complex reasoning, multi-step actions, or external tools, DO NOT create a monolithic script. Instead, decompose the skill into a multi-agent DAG (Directed Acyclic Graph) using subagents with strictly defined, schema-validated state handoffs.
- **Council Evaluation:** If the requested skill is highly complex or high-stakes, invoke the `storm-council` skill to uncover edge cases, architectural flaws, and required constraints before drafting.

### 3. Grounded Drafting
Draft the new `SKILL.md`. If it is a modular pipeline, explicitly define the subagent roles, their specific inputs/outputs, and the orchestration mechanism to ensure traceability.

**Mandatory Self-Containedness Standard:**
Every skill MUST adhere to the following file structure to guarantee it is self-contained:
- **`scripts/`**: All executable code (Python, Bash, Pixi environments) required for deterministic/repetitive tasks MUST be placed here. Do not instruct the agent to run complex arbitrary shell commands if a script can handle it reliably.
- **State Referee Template (CRITICAL):** You MUST force the new skill into a deterministic state machine using the universal template.
  1. Copy `/home/rcrede/.gemini/config/skills/skill-creator/templates/state_referee_template.py` to `scripts/<skill>_referee.py` in the new skill's directory.
  2. Create a `scripts/referee_config.json` defining the execution phases and `MANDATORY TOOL CONSTRAINTS` for the new skill.
  3. You MUST write the new skill's `SKILL.md` such that it explicitly forces the agent to run `python scripts/<skill>_referee.py init` and `advance --to [NEXT_PHASE]` instead of relying on unstructured prompt instructions.
- **`standards/`**: Every skill MUST have a `standards/` directory containing an `.md` file specifying its execution rules, formatting, and behavior. This standard `.md` file MUST ALWAYS be symlinked to the user's Obsidian Vault at `80_System/Standards/` during the creation process (e.g., `ln -s /path/to/skill/standards/my_standard.md "/home/rcrede/Documents/Obsidian Vault/80_System/Standards/"`).

### 4. Automated Reflect-Extract-Inject Loop
This is the core automation engine. Do not involve the user until this loop completes.
1. **Trace Execution:** Spawn a subagent to run the drafted skill against the "Train" test cases.
2. **Reflect (Diagnostic Feedback):** Spawn a specialized reviewer subagent to analyze the execution traces. Use granular, multidimensional metrics (e.g., adherence to constraints, parsing precision, hallucination rate) rather than binary pass/fail. If it is a multi-agent pipeline, evaluate intermediate steps, not just the final output.
3. **Extract (Skill Extraction):** Extract concrete failure modes. Why did the test fail? Which subagent hallucinated? 
4. **Inject (Auto-Iteration):** Propose and apply automated fixes to the `SKILL.md` (or its subagent prompts) to resolve the extracted failures. Ensure a rollback mechanism is in place if the injection introduces regressions.
*Repeat this loop until the Train set passes or a maximum of 3 iterations is reached.*

### 5. Benchmark Analysis & Executive Summary
Once the loop concludes, test the refined skill against the hidden "Validation" set. 
Present an Executive Summary to the user, strictly containing:
- **Performance Report:** The pass rate on the validation set.
- **Actionable Insights:** Why certain tests failed (with direct links to traces or verifiable diffs).
- **Recommended Injections:** A list of the automated changes made during the loop for the human to review and rubber-stamp. Do not hallucinate narratives; stick to grounded, factual execution logs.
