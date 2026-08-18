#!/usr/bin/env python3
"""
validate_inputs.py — Verify that a paper-orchestra workspace has the four
required input files in the correct place and minimally well-formed.

This is a deterministic structural check. It does NOT call an LLM, does NOT
talk to the network, and does NOT validate semantic content — that is the
job of the Outline Agent itself.

Exit codes:
    0  all checks passed
    1  one or more required inputs missing or malformed

Usage:
    python validate_inputs.py --paperorchestra /path/to/paperorchestra/
"""
import argparse
import os
import re
import sys

REQUIRED_INPUTS = [
    "template.typ",
]


def check_file_exists(path: str) -> list[str]:
    if not os.path.isfile(path):
        return [f"MISSING: {path}"]
    if os.path.getsize(path) == 0:
        return [f"EMPTY: {path}"]
    return []


def check_ara_logic(path: str) -> list[str]:
    errors = check_file_exists(path)
    if errors:
        return errors
    text = open(path).read()
    if not re.search(r"\*\*Statement\*\*", text, re.M):
        return ["WARN: ara/logic/claims.md missing '**Statement**' blocks"]
    return []


def check_ara_evidence(path: str) -> list[str]:
    errors = check_file_exists(path)
    if errors:
        return errors
    return []


def check_template(path: str) -> list[str]:
    errors = check_file_exists(path)
    if errors:
        return errors
    text = open(path).read()
    if "#set document" not in text and "= " not in text:
        return [f"ERROR: {path} does not look like a Typst document"]
    return []


def check_guidelines(path: str) -> list[str]:
    errors = check_file_exists(path)
    if errors:
        return errors
    text = open(path).read().lower()
    out = []
    if "page" not in text:
        out.append("WARN: conference_guidelines.md does not mention 'page' — "
                   "page limit unclear")
    if "deadline" not in text and "cutoff" not in text and "submission" not in text:
        out.append("WARN: conference_guidelines.md does not mention a deadline / "
                   "cutoff — literature review agent will not be able to scope citations")
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--paperorchestra", required=True, help="Path to the workspace directory")
    p.add_argument("--ara", required=False, default="ara", help="Path to the ARA directory")
    args = p.parse_args()

    ws = os.path.abspath(args.workspace)
    ara_dir = os.path.abspath(args.ara)
    inputs = os.path.join(ws, "inputs")
    if not os.path.isdir(inputs):
        print(f"ERROR: {inputs} does not exist. Run init_workspace.py first.",
              file=sys.stderr)
        return 1

    all_problems: list[str] = []
    
    # Check ARA
    problems = check_ara_logic(os.path.join(ara_dir, "logic", "claims.md"))
    all_problems.extend(problems)
    problems = check_ara_evidence(os.path.join(ara_dir, "evidence", "README.md"))
    all_problems.extend(problems)

    # Check Workspace Inputs
    checks = {
        "template.typ":             check_template,
    }
    for fname, fn in checks.items():
        problems = fn(os.path.join(inputs, fname))
        for p_ in problems:
            all_problems.append(p_)

    figs = os.path.join(inputs, "figures")
    if os.path.isdir(figs):
        n_figs = len([f for f in os.listdir(figs) if f.lower().endswith((".png", ".pdf", ".jpg", ".jpeg"))])
        print(f"INFO: {n_figs} pre-existing figure(s) in inputs/figures/")
    else:
        print("INFO: no inputs/figures/ — plotting agent will generate everything")

    if not all_problems:
        print("OK: all 4 required inputs present and well-formed.")
        return 0

    fatal = [p for p in all_problems if p.startswith("ERROR") or p.startswith("MISSING") or p.startswith("EMPTY")]
    warn = [p for p in all_problems if p.startswith("WARN")]
    for p_ in fatal:
        print(p_, file=sys.stderr)
    for p_ in warn:
        print(p_)
    return 1 if fatal else 0


if __name__ == "__main__":
    sys.exit(main())
