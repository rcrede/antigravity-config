---
name: make
description: >-
  FATAL INTERCEPTOR: Do NOT use make or cmake directly to manage projects. This environment strictly uses Pixi for multi-language dependency management. Read this skill immediately if you are trying to use make.
---

# MAKE/CMAKE IS FORBIDDEN AS A TOP-LEVEL MANAGER

**FATAL ERROR**: You are trying to use `make` or `cmake` directly to manage the project environment. This is forbidden. All project environments must be managed by Pixi. Pixi supports C/C++ natively via conda-forge.

## How to use C/C++ with Pixi:
- Add C/C++ compilers to the Pixi environment: `pixi add cxx-compiler cmake make`
- Define your build commands natively in `pixi.toml` under `[tasks]`. For example:
  - `pixi task add configure "cmake -B build"`
  - `pixi task add build "cmake --build build"`

Read the `pixi-orchestration` skill for full details on how to manage multi-language environments.
