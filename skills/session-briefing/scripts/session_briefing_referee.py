import argparse
import json
import os
import sys

STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"phase": "INIT", "diff_output": "", "project_state": ""}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def init(workspace_dir):
    state = load_state()
    state["phase"] = "DIFF_PHASE"
    save_state(state)
    print("STATE: DIFF_PHASE")
    print(f"ACTION: Use `run_command` to execute `git diff HEAD~1` or `git status` in the workspace directory '{workspace_dir}'.")
    print("ACTION: Submit the output to the referee using `pixi run python session_briefing_referee.py submit_diff --output \"<diff_text>\"`")
    print("MANDATORY TOOL CONSTRAINT: You may only use `run_command` to get the diff, and `run_command` to submit the diff. Do not write the final synthesis yet.")

def submit_diff(output):
    state = load_state()
    if state["phase"] != "DIFF_PHASE":
        print(f"ERROR: Expected DIFF_PHASE, got {state['phase']}")
        sys.exit(1)
    state["diff_output"] = output
    state["phase"] = "RETRIEVAL_PHASE"
    save_state(state)
    print("STATE: RETRIEVAL_PHASE")
    print("ACTION: Based on the diff, identify the active project markdown file. Use `view_file` to read its YAML frontmatter and task list.")
    print("ACTION: Submit the project state using `pixi run python session_briefing_referee.py submit_project_state --state \"<yaml_and_tasks>\"`")
    print("MANDATORY TOOL CONSTRAINT: Only use `view_file` to read the project file, and `run_command` to submit the state.")

def submit_project_state(project_state):
    state = load_state()
    if state["phase"] != "RETRIEVAL_PHASE":
        print(f"ERROR: Expected RETRIEVAL_PHASE, got {state['phase']}")
        sys.exit(1)
    state["project_state"] = project_state
    state["phase"] = "SYNTHESIS_PHASE"
    save_state(state)
    print("STATE: SYNTHESIS_PHASE")
    print("ACTION: You have all the data. Present a concise 'Welcome Back' message to the user summarizing what changed manually and proposing the next atomic action.")
    print("ACTION: Run `pixi run python session_briefing_referee.py complete` when you are done.")

def complete():
    state = load_state()
    state["phase"] = "COMPLETED"
    save_state(state)
    print("STATE: COMPLETED")
    print("Session Briefing is complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--workspace", type=str, default=".")
    
    diff_parser = subparsers.add_parser("submit_diff")
    diff_parser.add_argument("--output", type=str, required=True)
    
    state_parser = subparsers.add_parser("submit_project_state")
    state_parser.add_argument("--state", type=str, required=True)
    
    subparsers.add_parser("complete")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init(args.workspace)
    elif args.command == "submit_diff":
        submit_diff(args.output)
    elif args.command == "submit_project_state":
        submit_project_state(args.state)
    elif args.command == "complete":
        complete()
    else:
        parser.print_help()
