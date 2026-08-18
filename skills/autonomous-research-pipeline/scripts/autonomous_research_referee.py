import argparse
import json
import os
import sys

STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"phase": "INIT"}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def init():
    state = load_state()
    state["phase"] = "WORKSPACE_INIT_PHASE"
    save_state(state)
    print("STATE: WORKSPACE_INIT_PHASE")
    print("ACTION: Use `pixi-orchestration` to initialize a new repository.")
    print("ACTION: Ensure strict System vs User split (01_scripts, 02_notebooks, 03_data, 04_reports).")
    print("ACTION: Initialize Git and run MapWeaver.")
    print("ACTION: Run `pixi run python autonomous_research_referee.py advance --to MARIMO` when done.")
    print("MANDATORY TOOL CONSTRAINT: Use appropriate tools for setup. Do not write computational logic yet.")

def advance(to_phase):
    state = load_state()
    valid_transitions = {
        "WORKSPACE_INIT_PHASE": "MARIMO",
        "MARIMO_PHASE": "HOUSEKEEPING",
        "HOUSEKEEPING_PHASE": "ARA_HANDOFF",
        "ARA_HANDOFF_PHASE": "DISSEMINATION",
        "DISSEMINATION_PHASE": "COMPLETED"
    }
    
    if valid_transitions.get(state["phase"]) != to_phase:
        print(f"ERROR: Cannot advance from {state['phase']} to {to_phase}")
        sys.exit(1)
        
    state["phase"] = f"{to_phase}_PHASE"
    save_state(state)
    
    if to_phase == "MARIMO":
        print("STATE: MARIMO_PHASE")
        print("ACTION: Write core logic in `01_scripts/` as testable Python functions.")
        print("ACTION: Write interactive UI in `02_notebooks/` using `marimo`.")
        print("ACTION: Define `pixi run` tasks for both in `pixi.toml`.")
        print("ACTION: Run `pixi run python autonomous_research_referee.py advance --to HOUSEKEEPING` when scripts are ready.")
    elif to_phase == "HOUSEKEEPING":
        print("STATE: HOUSEKEEPING_PHASE")
        print("ACTION: Trigger `MapWeaver` builder to update `CODEMAP.md`.")
        print("ACTION: Perform an ultra-granular `git commit` to preserve state.")
        print("ACTION: Run `pixi run python autonomous_research_referee.py advance --to ARA_HANDOFF`.")
    elif to_phase == "ARA_HANDOFF":
        print("STATE: ARA_HANDOFF_PHASE")
        print("ACTION: Spawn a dedicated subagent (TypeName: self) as 'Live PM'.")
        print("ACTION: Instruct it to explicitly use `research-manager` to harvest logic into `ara/`.")
        print("ACTION: Verify `ara/logic/` and `ara/evidence/` exist.")
        print("ACTION: Run `pixi run python autonomous_research_referee.py advance --to DISSEMINATION` when verified.")
    elif to_phase == "DISSEMINATION":
        print("STATE: DISSEMINATION_PHASE")
        print("ACTION: Invoke `paper-orchestra` to compile the final paper.")
        print("ACTION: Move the PDF from `paperorchestra/main.pdf` to `04_reports/final_report.pdf`.")
        print("ACTION: Run `pixi run python autonomous_research_referee.py advance --to COMPLETED` when complete.")
    elif to_phase == "COMPLETED":
        print("STATE: COMPLETED")
        print("Autonomous Research Pipeline complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("init")
    
    advance_parser = subparsers.add_parser("advance")
    advance_parser.add_argument("--to", type=str, required=True, choices=["MARIMO", "HOUSEKEEPING", "ARA_HANDOFF", "DISSEMINATION", "COMPLETED"])
    
    args = parser.parse_args()
    
    if args.command == "init":
        init()
    elif args.command == "advance":
        advance(args.to)
    else:
        parser.print_help()
