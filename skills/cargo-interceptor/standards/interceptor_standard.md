---
date created: 2026-07-16T20:25:00+02:00
---

# Interceptor Standard

This standard dictates the rules for all Interceptor skills (`pip`, `cargo`, `make`, `markdown`).

**1. Never execute the intercepted command:** The agent must immediately abort the attempted action that triggered this skill. 
**2. Always redirect to the approved tool:** The agent must redirect the user or itself to the approved, deterministic alternative (e.g., Pixi for package management).
**3. Must provide immediate failure feedback:** The agent must clearly state in chat that the action was intercepted due to environmental safety constraints.
