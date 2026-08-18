import argparse
import json
import os
import sys

STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"phase": "INIT", "scope_tag": "", "graph_data": ""}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def init(scope_tag):
    state = load_state()
    state["phase"] = "EXTRACT_PHASE"
    state["scope_tag"] = scope_tag
    save_state(state)
    print("STATE: EXTRACT_PHASE")
    print(f"ACTION: Run `scripts/extract_graph.py <path_to_vault> {scope_tag}` to get the sub-graph JSON.")
    print("ACTION: Submit the JSON using `pixi run python sota_synthesis_referee.py submit_graph --data \"<json>\"`")
    print("MANDATORY TOOL CONSTRAINT: Use `run_command` only.")

def submit_graph(data):
    state = load_state()
    if state["phase"] != "EXTRACT_PHASE":
        print(f"ERROR: Cannot submit graph in phase {state['phase']}")
        sys.exit(1)
        
    state["graph_data"] = data
    state["phase"] = "ANALYSIS_PHASE"
    save_state(state)
    print("STATE: ANALYSIS_PHASE")
    print("ACTION: Construct an internal map linking DSLNs to Zettels. Identify hubs, missing edges, and contradictions.")
    print("ACTION: Once analyzed, run `pixi run python sota_synthesis_referee.py advance --to REPORT`.")

def advance(to_phase):
    state = load_state()
    if state["phase"] == "ANALYSIS_PHASE" and to_phase == "REPORT":
        state["phase"] = "REPORT_PHASE"
        save_state(state)
        print("STATE: REPORT_PHASE")
        print("ACTION: Draft `State_Of_The_Art_Report.md` containing Consensus Claims, Contradictions, and Identified Gaps.")
        print("ACTION: Once saved, run `pixi run python sota_synthesis_referee.py advance --to COMPLETED`.")
    elif state["phase"] == "REPORT_PHASE" and to_phase == "COMPLETED":
        state["phase"] = "COMPLETED"
        save_state(state)
        print("STATE: COMPLETED")
        print("SOTA Synthesis complete.")
    else:
        print(f"ERROR: Invalid transition from {state['phase']} to {to_phase}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--scope", type=str, required=True)
    
    submit_parser = subparsers.add_parser("submit_graph")
    submit_parser.add_argument("--data", type=str, required=True)
    
    advance_parser = subparsers.add_parser("advance")
    advance_parser.add_argument("--to", type=str, required=True, choices=["REPORT", "COMPLETED"])
    
    args = parser.parse_args()
    
    if args.command == "init":
        init(args.scope)
    elif args.command == "submit_graph":
        submit_graph(args.data)
    elif args.command == "advance":
        advance(args.to)
    else:
        parser.print_help()
