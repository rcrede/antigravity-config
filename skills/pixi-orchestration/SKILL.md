---
name: pixi-orchestration
description: >-
  Manage project dependencies, task pipelines, and development environments using Pixi. 
  Use this skill WHENEVER you need to manage dependencies, install packages, write scratch scripts, 
  or structure a project in Python, Rust, C++, or other supported languages. Use it whenever you see 
  a chain of CLI commands or a complex workflow that could be turned into repeatable Pixi tasks.
  Ensure that any coding project capable of being managed by Pixi IS managed by Pixi.
---

# Pixi Orchestration Skill

To ensure reproducible, multi-environment, and cleanly abstracted computational pipelines, you must use `pixi` as the primary orchestrator for all supported coding projects.

## 1. When to Use
- **Always Default to Pixi**: If you need to install a package (e.g., Python, Rust, C++ tools), use Pixi instead of global package managers, `pip`, or `conda` directly. 
- **Scratch Scripts**: Even if you are just writing a quick scratch script, initialize a Pixi workspace for it.
- **Complex Workflows**: Any complex shell workflow, command chain, or build step MUST be converted into a deterministic `pixi` task.

## 2. Managing Environments & Dependencies
- **CLI First**: Prefer using the `pixi` CLI to add packages and tasks (e.g., `pixi add pandas`, `pixi task add run "python main.py"`). This allows the Pixi backend to safely resolve dependencies.
- **PyPI Dependencies**: Do NOT install `pip` with `pixi` or run manual `pip install` commands. Pixi handles PyPI dependencies natively! If you need a remote PyPI package, use `pixi add --pypi <package_name>`. If you need to install a local Python package (the equivalent of `pip install -e .`), use `pixi add --pypi "package_name @ ./local/path"`. Never fall back to `pip`.
- **Manual Editing**: Only edit the `pixi.toml` file manually when absolutely necessary (e.g., setting up complex multi-environments, advanced templating, or bulk dependency additions).
- **Multi-Environment Configuration**: When applicable (e.g., separating `dev`, `test`, and `prod` dependencies), you must explicitly configure `[environments]` and `[feature]` groups in `pixi.toml`.

## 3. Task Pipelines & Caching
- **Semantic Tasks**: Never write raw bash scripts for orchestrating project steps. Instead, define semantic tasks in `pixi.toml` (e.g., `pixi run solvate`, `pixi run test`).
- **Dependencies & Caching**: When building task pipelines, leverage `depends-on` to chain tasks together. Define `inputs` and `outputs` arrays for each task to enable native caching and prevent redundant execution.

## 4. Multi-Language Support
- Pixi supports multiple ecosystems via `conda-forge`. When working in a multi-language repository (e.g., Python + Rust), install the respective toolchains (e.g., `python`, `rust`, `cargo`) natively into the `pixi.toml` workspace so that the environments are completely isolated and self-contained.

## 5. Project Documentation
Whenever initializing a new Pixi workspace or restructuring a repository, you MUST explicitly determine the project type and load the appropriate documentation standard bundled with this skill:
- **For Scientific/Research Projects:** Read and adhere to **`standards/scientific_repo_documentation_standard.md`**. This enforces the strict Agent-Native Research Artifact (ARA) structure (`ara/logic/`, `ara/trace/`) and Google Antigravity SDK CI/CD pipelines.
- **For Hobby/General Projects:** Read and adhere to **`standards/general_repo_standard.md`**. This ensures clean `README.md` and `CONTRIBUTING.md` setups and Pixi task isolation without the heavy ARA scaffolding overhead.
