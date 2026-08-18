---
name: general-repo-standard
description: >-
  Standardized rules for organizing generic code repositories and hobby projects,
  focusing on clean READMEs and Pixi task isolation without enforcing heavy ARA pipelines.
date created: 2026-07-09T02:36:17+02:00
date modified: 2026-07-09T23:59:04+02:00
---

## General Repository Standard (Pixi)

When initializing or organizing a code repository that is NOT a strict PaperOrchestra/ARA scientific project (e.g., hobby projects, generic software tools, utility scripts), you must adhere to the following clean-code guidelines.

### 1. Project Orchestration (`pixi.toml`)

- **Always Default to Pixi**: Use Pixi to manage environments, dependencies, and toolchains (Python, Rust, C++) to ensure perfect reproducibility.
- **Semantic Tasks**: Never write raw bash execution scripts inside documentation. Define semantic tasks in `pixi.toml` (e.g., `pixi run build`, `pixi run test`, `pixi run start`).
- **Isolation**: When working in a multi-language repository, install the respective toolchains natively into the `pixi.toml` workspace so environments are completely self-contained.

### 2. The Human Layer (`README.md`)

- The project root must contain a comprehensive `README.md`.
- **Purpose:** Executive summary, installation instructions, usage examples, and architecture overview.
- **Usage Section:** Explicitly list the available `pixi` tasks needed to run the project.

### 3. The Developer Layer (`CONTRIBUTING.md`)

- If the project is meant for collaboration, include a `CONTRIBUTING.md`.
- Detail how to set up the dev environment (`pixi install`), run the linters, and execute the test suite (`pixi run test`).

### 4. When to Use ARA (Escalation)

- This standard governs *general* projects.
- If the user explicitly requests an Agent-Native Research Artifact, a scientific paper, or an epistemic trace, escalate to the `repo_documentation_standard.md` which enforces the strict `ara/` directory layout and Google Antigravity SDK CI/CD pipelines.
