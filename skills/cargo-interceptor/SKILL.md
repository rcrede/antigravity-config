---
name: cargo
description: >-
  FATAL INTERCEPTOR: Do NOT use cargo directly to manage projects. This environment strictly uses Pixi for multi-language dependency management. Read this skill immediately if you are trying to use Cargo.
---

# CARGO IS FORBIDDEN AS A TOP-LEVEL MANAGER

**FATAL ERROR**: You are trying to use `cargo` directly. This is forbidden. All project environments must be managed by Pixi. Pixi supports Rust natively via conda-forge.

## How to use Rust with Pixi:
- Add Rust to the Pixi environment: `pixi add rust cargo`
- Define your cargo build/run commands natively in `pixi.toml` under `[tasks]`. For example:
  - `pixi task add build "cargo build"`
  - `pixi task add run "cargo run"`

Read the `pixi-orchestration` skill for full details on how to manage multi-language environments.
