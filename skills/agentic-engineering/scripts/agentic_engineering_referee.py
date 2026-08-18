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
    state["phase"] = "EVAL_PHASE"
    save_state(state)
    print("STATE: EVAL_PHASE")
    print("ACTION: Define capability and regression evals (tests) for the current assigned unit from the Design Document.")
    print("ACTION: Run baseline test and capture failure signatures (Red phase).")
    print("ACTION: Run `pixi run python agentic_engineering_referee.py advance --to IMPLEMENTATION` when evals fail as expected.")

def advance(to_phase):
    state = load_state()
    valid_transitions = {
        "EVAL_PHASE": "IMPLEMENTATION",
        "IMPLEMENTATION_PHASE": "VERIFICATION",
        "VERIFICATION_PHASE": ["EVAL", "COMPLETED"] # Loop back for retry/next unit, or finish
    }
    
    allowed = valid_transitions.get(state["phase"])
    if isinstance(allowed, list):
        if to_phase not in allowed:
            print(f"ERROR: Cannot advance from {state['phase']} to {to_phase}")
            sys.exit(1)
    else:
        if allowed != to_phase:
            print(f"ERROR: Cannot advance from {state['phase']} to {to_phase}")
            sys.exit(1)
            
    state["phase"] = f"{to_phase}_PHASE"
    save_state(state)
    
    if to_phase == "EVAL":
        print("STATE: EVAL_PHASE")
        print("ACTION: Define capability and regression evals for the current unit.")
        print("ACTION: Run baseline and capture failure signatures.")
        print("ACTION: Run `pixi run python agentic_engineering_referee.py advance --to IMPLEMENTATION` when evals are ready.")
    elif to_phase == "IMPLEMENTATION":
        print("STATE: IMPLEMENTATION_PHASE")
        print("ACTION: Execute implementation.")
        print("ACTION: Run `pixi run python agentic_engineering_referee.py advance --to VERIFICATION` when implemented.")
    elif to_phase == "VERIFICATION":
        print("STATE: VERIFICATION_PHASE")
        print("ACTION: Re-run evals and verify improvements.")
        print("ACTION: Review code focusing on invariants, edge cases, error boundaries, security, coupling.")
        print("ACTION: Track cost (tier, tokens, retries, time, outcome).")
        print("ACTION: If more units remain, run `pixi run python agentic_engineering_referee.py advance --to EVAL`.")
        print("ACTION: If all units are done, run `pixi run python agentic_engineering_referee.py advance --to COMPLETED`.")
    elif to_phase == "COMPLETED":
        print("STATE: COMPLETED")
        print("Agentic Engineering workflow complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("init")
    
    advance_parser = subparsers.add_parser("advance")
    advance_parser.add_argument("--to", type=str, required=True, choices=["EVAL", "IMPLEMENTATION", "VERIFICATION", "COMPLETED"])
    
    args = parser.parse_args()
    
    if args.command == "init":
        init()
    elif args.command == "advance":
        advance(args.to)
    else:
        parser.print_help()
