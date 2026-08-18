---
name: pip
description: >-
  FATAL INTERCEPTOR: Do NOT use pip. This environment strictly uses Pixi for dependency management. Read this skill immediately if you are trying to install a python package.
---

# PIP IS FORBIDDEN

**FATAL ERROR**: You are trying to use `pip`. This is strictly forbidden in this environment. All project dependencies must be managed by Pixi to ensure deterministic, containerized environments.

## How to add Python packages:
Instead of running `pip install`, you MUST use the `pixi` CLI:
- To add a remote PyPI package: `pixi add --pypi <package_name>`
- To add a local directory (equivalent to `pip install -e .`): `pixi add --pypi "package_name @ ./local/path"`

Read the `pixi-orchestration` skill for full details on how to manage dependencies and task pipelines.
