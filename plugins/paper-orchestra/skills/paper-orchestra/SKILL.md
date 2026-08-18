---
name: paper-orchestra
description: Orchestrate the full PaperOrchestra (Song et al., 2026, arXiv:2604.05018) five-agent pipeline to turn unstructured research materials (idea, experimental log, LaTeX template, conference guidelines, optional figures) into a submission-ready LaTeX manuscript and compiled PDF. TRIGGER when the user asks to "write a paper from my experiments", "turn this idea and these results into a paper", "generate a conference submission", "run paper-orchestra on X", or otherwise wants the end-to-end paper-writing pipeline. Coordinates the outline-agent, plotting-agent, literature-review-agent, section-writing-agent, and content-refinement-agent skills.
data_access_level: raw
---

# paper-orchestra (Orchestrator)

Top-level driver for the PaperOrchestra pipeline. Read this document and follow
the steps below. The detailed prompts and rules live in each sub-skill's
`SKILL.md` and `references/` directories — you (the host agent) will load them
as you go.

> Source paper: Song et al., *PaperOrchestra: A Multi-Agent Framework for
> Automated AI Research Paper Writing*, arXiv:2604.05018, 2026.
> <https://arxiv.org/pdf/2604.05018>

## What this skill produces

A complete submission package `P = (paper.tex, paper.pdf)` written into
`paperorchestra/final/`, plus a full audit trail under `paperorchestra/` (outline,
figures, refs, drafts, refinement worklog, provenance snapshot).

## Inputs (the (A, T, G, F) tuple)

The workspace MUST contain:

| File | Symbol | Required | Description |
|---|---|---|---|
| `ara/` directory | `A` | yes | The completed Agent-Native Research Artifact (logic/ and evidence/) |
| `paperorchestra/inputs/template.typ` | `T` | yes | Typst template for the target conference |
| `paperorchestra/inputs/conference_guidelines.md` | `G` | yes | Formatting rules, page limit, mandatory sections |
| `paperorchestra/inputs/figures/` | `F` | no | Optional pre-existing figures. If empty, the plotting agent generates everything. |

`scripts/init_workspace.py` will scaffold this layout. `scripts/validate_inputs.py`
will check it before the pipeline runs.

## Pipeline (read `references/pipeline.md` for the full diagram)

```
Step 1: Outline           ──▶  outline.json                       (1 LLM call)
Step 2: Plotting     ─┐
                      ├──▶  figures/*.png + captions.json         (~20-30 calls)
Step 3: Lit Review   ─┘                                           (~20-30 calls)
                          intro_relwork.typ + refs.bib

Step 4: Section Writing  ──▶  drafts/paper.typ                    (1 LLM call)
Step 5: Content Refine   ──▶  final/main.typ + final/main.pdf   (~5-7 calls, ~3 iters)
```

Step 2 and Step 3 are independent and **MUST run in parallel** when your host
supports parallel sub-agents. If not, run Step 3 first (it has the longer wall
time due to Semantic Scholar rate limits) and Step 2 second.

## Critical pre-instruction (read once, apply always)

Before any LLM call that *writes* paper content (outline, intro/related work,
section writing, refinement), you MUST prepend the **Anti-Leakage Prompt** at
`references/anti-leakage-prompt.md` to your system prompt. This is verbatim
from Appendix D.4 of the paper and prevents pre-training-data leakage. The
paper applies it uniformly across all baselines for fair comparison; we apply
it for fidelity *and* to keep generated papers grounded in the user's inputs.

## Step-by-step execution

### 0. Pre-flight Checks

Before running the pipeline, perform the following quality gates in order:

```bash
# 1. Scaffold the workspace
python skills/paper-orchestra/scripts/init_workspace.py --out paperorchestra/
# user drops their inputs into paperorchestra/inputs/

# 2. Validate required files are present and well-formed
python skills/paper-orchestra/scripts/validate_inputs.py --paperorchestra paperorchestra/ --ara ara/
```

If `validate_inputs.py` fails (exit code 1 or 2), stop
and tell the user what's missing or below threshold — do not proceed until fixed.

`validate_consistency.py` produces warnings only (exit code 1 = WARN, non-blocking);
report warnings to the user but continue.

**Before failing on missing inputs**, check whether the `ara/` directory exists. If it does not exist, run the ARA `research-manager` to compile it.

### 1. Outline (Step 1 — 1 LLM call)

Load `skills/outline-agent/SKILL.md` and follow it. Output: `paperorchestra/outline.json`.
Validate with `python skills/outline-agent/scripts/validate_outline.py paperorchestra/outline.json`.
**Halt the pipeline if validation fails** — every downstream agent depends on the schema.

### 2 ∥ 3. Plotting and Literature Review (in parallel)

Parse `outline.json`. Extract:
- `outline.plotting_plan` → drives Step 2
- `outline.intro_related_work_plan` → drives Step 3

If your host supports parallel sub-agents (Claude Code's Agent tool with multiple
concurrent calls; Cursor's parallel agents; Antigravity's worker pool), spawn
**two concurrent sub-tasks**:

- Sub-task A: load `skills/plotting-agent/SKILL.md`, execute the plotting plan,
  produce `paperorchestra/figures/<figure_id>.png` for every entry, plus
  `paperorchestra/figures/captions.json`.
- Sub-task B: load `skills/literature-review-agent/SKILL.md`, execute the
  research strategy, produce `paperorchestra/drafts/intro_relwork.typ` and
  `paperorchestra/refs.bib`.

If your host does not support parallel sub-agents, run Sub-task B first (it has
slower wall-clock due to Semantic Scholar QPS limits) then Sub-task A. The
artifacts are independent, so order doesn't affect correctness.

### 3.5. Outline Reconciliation (after Step 3 completes, before Step 4)

Once Step 3 (Literature Review) has produced `citation_pool.json` and
`cross_verification_report.json`, run the reconciliation step.

Load `references/outline-reconciliation.md` and follow its prompt.
Output: `paperorchestra/outline_reconciled.json`.

Validate and diff:

```bash
python skills/outline-agent/scripts/validate_outline.py paperorchestra/outline_reconciled.json
python skills/paper-orchestra/scripts/diff_outlines.py \
    --original   paperorchestra/outline.json \
    --reconciled paperorchestra/outline_reconciled.json \
    --summary    paperorchestra/reconciliation_summary.md
```

If validation fails, fall back to `outline.json` for Step 4 and warn the user.
Show the user the `reconciliation_summary.md` (even if no changes — it confirms
the outline matched the actual literature).

**Skip conditions:** citation pool empty, Step 3 failed, or Step 2 is still
running and the host cannot issue another call concurrently. See
`references/outline-reconciliation.md` for full skip conditions.

### 4. Section Writing (Step 4 — ONE single multimodal LLM call)

Load `skills/section-writing-agent/SKILL.md` and follow it. This is **one
single call** in the paper (App. B: "Section Writing Agent (1 call)") — do
*not* split it per section. The agent receives:

- `outline_reconciled.json` (use this if it exists; fall back to `outline.json`)
- `ara/` directory (logic and evidence)
- `intro_relwork.typ` (already-filled from Step 3 — preserve verbatim)
- `refs.bib` (the citation map)
- `conference_guidelines.md`
- `research_brief.md` (if it exists — read §1–§3 for accumulated pipeline context)
- The actual figure image files from `paperorchestra/figures/` (multimodal input)

Output: `paperorchestra/drafts/paper.typ` (a complete Typst document).

Then run the deterministic gates:

```bash
typst compile paperorchestra/drafts/paper.typ
python skills/paper-orchestra/scripts/anti_leakage_check.py paperorchestra/drafts/paper.typ
```

If any gate fails, the host agent must fix the issue (re-prompting the writing
step with the gate's error report) before proceeding.

### 5. Content Refinement (Step 5 — ~3 iterations, ~5-7 calls)

Load `skills/content-refinement-agent/SKILL.md` and follow it. The skill
implements the loop with strict halt rules from `halt-rules.md`. Maintain
`paperorchestra/refinement/worklog.json` and snapshot each iteration into
`paperorchestra/refinement/iter<N>/`.

Halt conditions (any one triggers the loop to stop and accept the current
best snapshot):

1. Iteration count reaches the cap (default 3, see `halt-rules.md`).
2. Overall score from the simulated reviewer **decreases** vs the previous
   iteration → revert to previous snapshot, halt.
3. Overall score **ties** but at least one sub-axis **decreases** while none
   gain compensatingly (negative net sub-axis change) → revert, halt.
4. Reviewer issues no new actionable weaknesses.

The accepted snapshot is copied to `paperorchestra/final/main.typ`.

### 6. Compile and finalize

```bash
cd paperorchestra/final && typst compile main.typ
```

Then write `paperorchestra/provenance.json` capturing input file hashes, outline
hash, refs hash, figure hashes, and final tex/pdf hashes (helper:
`scripts/snapshot.py` in the orchestrator scripts dir if you want a one-shot;
otherwise the host agent computes hashes inline).

Report to the user: the path to `paperorchestra/final/paper.pdf`, a brief summary of
which sections were drafted, citation count, refinement iterations completed,
and any gates that failed mid-pipeline.

## Workspace layout

See `references/io-contract.md`. Summary:

```
paperorchestra/
├── inputs/                          # user-provided
│   ├── template.typ
│   ├── conference_guidelines.md
│   └── figures/                     # optional pre-existing figures
├── outline.json                     # Step 1 output
├── figures/                         # Step 2 output
│   ├── <figure_id>.png
│   └── captions.json
├── refs.bib                         # Step 3 output
├── drafts/                          # Step 3 + Step 4 output
│   ├── intro_relwork.typ
│   └── paper.typ
├── refinement/                      # Step 5 working dir
│   ├── worklog.json
│   ├── iter1/
│   ├── iter2/
│   └── iter3/
├── final/                           # accepted snapshot + compiled PDF
│   ├── main.typ
│   └── main.pdf
└── provenance.json                  # input/output hashes for reproducibility
```

## Cost budget (from paper App. B)

Total: ~60–70 LLM calls per paper, ~40 minutes wall-time on the paper's setup.
Budget breakdown:

| Step | Calls |
|---|---|
| Outline | 1 |
| Plotting | ~20–30 |
| Literature Review | ~20–30 |
| Section Writing | 1 |
| Content Refinement | ~5–7 |

## Host integration

See `references/host-integration.md` for per-host invocation details (Claude
Code, Cursor, Antigravity, Cline, Aider, OpenCode).

## Resources

- `references/pipeline.md` — full step-by-step flow + parallelism rules + halt rules
- `references/io-contract.md` — workspace layout, input file schemas
- `references/anti-leakage-prompt.md` — verbatim from App. D.4, prepend to every writing call
- `references/paper-summary.md` — 1-page distillation of arXiv:2604.05018
- `references/host-integration.md` — per-host invocation guide
- `references/outline-reconciliation.md` — **NEW** Step 3.5 outline reconciliation protocol (AutoSci-inspired)
- `scripts/init_workspace.py` — scaffold workspace dir tree
- `scripts/validate_inputs.py` — verify (I, E, T, G) before running
- `scripts/anti_leakage_check.py` — grep draft for leaked author names/emails/affils
- `scripts/claim_evidence_gate.py` — **NEW** WARN gate: verify numeric claims in draft are grounded in experimental_log.md
- `scripts/diff_outlines.py` — **NEW** diff original vs reconciled outline; writes reconciliation_summary.md
- `skills/shared/research_brief_template.md` — **NEW** schema for paperorchestra/research_brief.md (accumulated cross-agent context)
