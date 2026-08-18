#!/usr/bin/env python3
import os
import sys
import json
import argparse
from pathlib import Path

# This is a generic State Referee Template.
# It expects a `referee_config.json` file in the same directory, which defines the phases.
# Example referee_config.json:
# {
#   "phases": ["INIT", "RESEARCH", "IMPLEMENT", "COMPLETED"],
#   "instructions": {
#       "INIT": {"action": "Start the task", "constraints": "NO_TOOLS"},
#       "RESEARCH": {"action": "Find context", "constraints": "READ_ONLY"}
#   }
# }

SCRIPT_DIR = Path(__file__).parent.resolve()
STATE_FILE = SCRIPT_DIR / "state.json"
CONFIG_FILE = SCRIPT_DIR / "referee_config.json"

def load_config():
    if not CONFIG_FILE.exists():
        print(f"Error: Missing config file {CONFIG_FILE}", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def load_state():
    if not STATE_FILE.exists():
        return None
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def print_status(config, phase):
    instructions = config.get("instructions", {}).get(phase, {})
    action = instructions.get("action", "No action specified.")
    constraints = instructions.get("constraints", "NONE")
    
    print(f"STATE: {phase}")
    print(f"ACTION: {action}")
    print(f"MANDATORY TOOL CONSTRAINT: {constraints}")
    print("-" * 40)
    print("Do not proceed to the next phase until you have completed the ACTION.")
    print("Obey all constraints.")

def init_referee():
    config = load_config()
    phases = config.get("phases", [])
    if not phases:
        print("Error: No phases defined in config.", file=sys.stderr)
        sys.exit(1)
        
    first_phase = phases[0]
    save_state({"current_phase": first_phase})
    print("Referee Initialized.")
    print_status(config, first_phase)

def advance_referee(target_phase):
    config = load_config()
    state = load_state()
    
    if not state:
        print("Error: No active state. Please run 'init' first.", file=sys.stderr)
        sys.exit(1)
        
    current_phase = state.get("current_phase")
    phases = config.get("phases", [])
    
    if current_phase not in phases:
        print(f"Error: Corrupted state. Unknown phase {current_phase}.", file=sys.stderr)
        sys.exit(1)
        
    if target_phase not in phases:
        print(f"Error: Unknown target phase {target_phase}.", file=sys.stderr)
        sys.exit(1)
        
    current_index = phases.index(current_phase)
    target_index = phases.index(target_phase)
    
    if target_index <= current_index:
        print(f"Error: Cannot advance to {target_phase} from {current_phase}. Moving backwards is forbidden.", file=sys.stderr)
        sys.exit(1)
        
    if target_index > current_index + 1:
        expected_next = phases[current_index + 1]
        print(f"Error: Cannot skip phase {expected_next}. You must advance sequentially.", file=sys.stderr)
        sys.exit(1)
        
    # Valid advance
    state["current_phase"] = target_phase
    save_state(state)
    print("Phase Advanced Successfully.")
    print_status(config, target_phase)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="State Referee for Subagent Execution")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    init_parser = subparsers.add_parser("init", help="Initialize the state machine to the first phase")
    
    advance_parser = subparsers.add_parser("advance", help="Advance to the next phase")
    advance_parser.add_argument("--to", required=True, help="The target phase name")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_referee()
    elif args.command == "advance":
        advance_referee(args.to)
