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
    state["phase"] = "INGESTION_PHASE"
    save_state(state)
    print("STATE: INGESTION_PHASE")
    print("ACTION: Invoke `markitdown-extractor` on target PDFs.")
    print("ACTION: Once complete, run `pixi run python agentic_literature_referee.py advance --to CONDENSATION`.")

def advance(to_phase):
    state = load_state()
    valid_transitions = {
        "INGESTION_PHASE": "CONDENSATION",
        "CONDENSATION_PHASE": "VERIFICATION",
        "VERIFICATION_PHASE": "SYNTHESIS",
        "SYNTHESIS_PHASE": "RIGOR_COUNCIL",
        "RIGOR_COUNCIL_PHASE": "COMPLETED"
    }
    
    if valid_transitions.get(state["phase"]) != to_phase:
        print(f"ERROR: Cannot advance from {state['phase']} to {to_phase}")
        sys.exit(1)
        
    state["phase"] = f"{to_phase}_PHASE"
    save_state(state)
    
    if to_phase == "CONDENSATION":
        print("STATE: CONDENSATION_PHASE")
        print("ACTION: Invoke `dual-sided-compiler` on Raw Markdown files.")
        print("ACTION: Once done, explicitly notify the user to review Zettels.")
        print("MANDATORY HALT: Pause pipeline until user confirms review.")
        print("ACTION: When user confirms, run `pixi run python agentic_literature_referee.py advance --to VERIFICATION`.")
    elif to_phase == "VERIFICATION":
        print("STATE: VERIFICATION_PHASE")
        print("ACTION: Explicitly search `40_Zettelkasten/` for `#zettel/unreviewed` within the scoping tag.")
        print("ACTION: If found, HALT and warn user. If clean, run `pixi run python agentic_literature_referee.py advance --to SYNTHESIS`.")
    elif to_phase == "SYNTHESIS":
        print("STATE: SYNTHESIS_PHASE")
        print("ACTION: Invoke `sota-synthesis-agent` with the scoping tag.")
        print("ACTION: Parse gaps from the generated report.")
        print("ACTION: Run `pixi run python agentic_literature_referee.py advance --to RIGOR_COUNCIL`.")
    elif to_phase == "RIGOR_COUNCIL":
        print("STATE: RIGOR_COUNCIL_PHASE")
        print("ACTION: For each gap, invoke `rigor-reviewer`.")
        print("ACTION: If it passes, invoke `storm-council`.")
        print("ACTION: Compile verdicts into final ranked research agenda.")
        print("ACTION: Run `pixi run python agentic_literature_referee.py advance --to COMPLETED` when done.")
    elif to_phase == "COMPLETED":
        print("STATE: COMPLETED")
        print("Agentic Literature Pipeline complete. Present agenda to user.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("init")
    
    advance_parser = subparsers.add_parser("advance")
    advance_parser.add_argument("--to", type=str, required=True, choices=["CONDENSATION", "VERIFICATION", "SYNTHESIS", "RIGOR_COUNCIL", "COMPLETED"])
    
    args = parser.parse_args()
    
    if args.command == "init":
        init()
    elif args.command == "advance":
        advance(args.to)
    else:
        parser.print_help()
