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
    state["phase"] = "EXTRACTION_PHASE"
    save_state(state)
    print("STATE: EXTRACTION_PHASE")
    print("ACTION: Invoke the `compiler` skill on the target Raw Markdown file.")
    print("ACTION: Extract claims, methods, and concepts as structured JSON.")
    print("ACTION: Run `pixi run python dual_sided_referee.py advance --to RIGOR_REVIEW` when done.")

def advance(to_phase):
    state = load_state()
    valid_transitions = {
        "EXTRACTION_PHASE": "RIGOR_REVIEW",
        "RIGOR_REVIEW_PHASE": "SCAFFOLD",
        "SCAFFOLD_PHASE": "COMPLETED"
    }
    
    if valid_transitions.get(state["phase"]) != to_phase:
        print(f"ERROR: Cannot advance from {state['phase']} to {to_phase}")
        sys.exit(1)
        
    state["phase"] = f"{to_phase}_PHASE"
    save_state(state)
    
    if to_phase == "RIGOR_REVIEW":
        print("STATE: RIGOR_REVIEW_PHASE")
        print("ACTION: Pass extracted claims to `rigor-reviewer` to evaluate flaws/overreaches.")
        print("ACTION: Append rigor scores and warnings to the extracted JSON data.")
        print("ACTION: Run `pixi run python dual_sided_referee.py advance --to SCAFFOLD` when done.")
    elif to_phase == "SCAFFOLD":
        print("STATE: SCAFFOLD_PHASE")
        print("ACTION: Run `scripts/scaffold_dsln.py <path_to_json> <dsln_dir> <zettel_dir> <scope_tag>`")
        print("ACTION: Use `replace_file_content` to fill `<!-- Agent will fill dense summary here -->` in the DSLN.")
        print("ACTION: Return absolute paths to the generated DSLN and Zettels.")
        print("ACTION: Run `pixi run python dual_sided_referee.py advance --to COMPLETED`.")
    elif to_phase == "COMPLETED":
        print("STATE: COMPLETED")
        print("Dual-Sided Compiler complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("init")
    
    advance_parser = subparsers.add_parser("advance")
    advance_parser.add_argument("--to", type=str, required=True, choices=["RIGOR_REVIEW", "SCAFFOLD", "COMPLETED"])
    
    args = parser.parse_args()
    
    if args.command == "init":
        init()
    elif args.command == "advance":
        advance(args.to)
    else:
        parser.print_help()
