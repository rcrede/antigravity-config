---
name: exam-studying
description: Evidence-based studying skill integrating Feynman technique, active recall quizzing, spaced repetition Anki generation, and rigorous Oral Exam simulations.
---

# Exam Studying Skill

This skill is designed to help the user study for exams or learn new complex concepts (e.g., Organic/Inorganic Chemistry, Computational Chemistry). It uses heavily evidence-backed methodologies: The Feynman Technique, Active Recall, and Spaced Repetition.

## Execution Requirements

**Crucial Constraint:** You must use the `exam_studying_referee.py` script to manage the state of the session. The script will dictate whether you are doing Feynman, Quizzing, Oral Exam, or Anki Generation.

1. **Initialization:** Run the script to start the workflow.
   ```bash
   cd /home/rcrede/.gemini/config/skills/exam-studying/scripts
   python3 exam_studying_referee.py init
   ```
2. **Follow Instructions:** The script will output `STATE`, `ACTION`, and `MANDATORY TOOL CONSTRAINT`.
3. **Advance:** When the user decides to switch modes or finishes a session, advance the state:
   ```bash
   python3 exam_studying_referee.py advance --to [NEXT_PHASE]
   ```
   (Valid targets: `FEYNMAN_TUTORIAL`, `ACTIVE_RECALL`, `ORAL_EXAM`, `ANKI_GENERATION`, `COMPLETED`)

## Operating Modes

1. **Feynman Tutorial:** Act as a Socratic tutor. Prompt the user to explain a new concept. Probe for gaps and simplify.
2. **Active Recall:** Provide practice questions (multiple choice or short answer) based on their vault notes (use `qmd` MCP server to fetch contexts). Do not give answers immediately.
3. **Oral Exam Simulator:** Roleplay as a strict professor. Ask deep, interconnected questions that push beyond the basic syllabus to prepare the user for extra credit situations. Grade strictly and maintain a performance log.
4. **Anki Generation:** After the user has understood a concept (often after Feynman), run this phase to extract the key facts into a CSV file formatted for Anki import (Front,Back). Save this to a scratch file or in the vault.

## Constraints
- Always fetch relevant context from the Obsidian Vault before quizzing or testing.
- Strictly follow the directives in `80_System/Standards/exam_studying_standard.md`.
