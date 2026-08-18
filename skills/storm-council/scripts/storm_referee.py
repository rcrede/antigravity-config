import argparse
import json
import os
import sys

STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"phase": "INIT", "proposal": "", "experts": {}, "reviews": {}, "num_experts": 5}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def validate_response(response):
    if not response or len(response.strip()) == 0:
        print("ERROR: Response is empty.")
        sys.exit(1)
    word_count = len(response.split())
    if word_count < 30:
        print(f"ERROR: Response is too short ({word_count} words). It must be at least 30 words. Possible hallucination or truncation.")
        sys.exit(1)

def init(proposal, num_experts):
    state = load_state()
    state["phase"] = "EXPERT_PHASE"
    state["proposal"] = proposal
    state["experts"] = {}
    state["reviews"] = {}
    state["num_experts"] = num_experts
    save_state(state)
    print("STATE: EXPERT_PHASE")
    print(f"ACTION: Define {num_experts} specific Personas to review this proposal.")
    print("ACTION: Use the `invoke_subagent` tool to spawn a subagent for each Persona. Ask them to critique the proposal from their perspective in under 250 words.")
    print("MANDATORY TOOL CONSTRAINT: During this phase, you are ONLY allowed to use the 'invoke_subagent' tool, and 'run_command' or 'write_to_file' to submit responses. You are strictly forbidden from taking action on the project files.")
    print("MANDATORY HALT: Stop and yield execution until all expert subagents have replied. Do not hallucinate their responses.")

def submit_expert(persona, response):
    state = load_state()
    if state["phase"] != "EXPERT_PHASE":
        print(f"ERROR: Expected state EXPERT_PHASE, but currently in {state['phase']}.")
        sys.exit(1)
    
    validate_response(response)
    
    state["experts"][persona] = response
    save_state(state)
    
    num_experts = len(state["experts"])
    target_experts = state.get("num_experts", 5)
    print(f"SUCCESS: Recorded expert '{persona}'. Total experts: {num_experts}.")
    
    if num_experts >= target_experts:
        print("NOTE: You have enough experts. You may run `pixi run python storm_referee.py advance_to_review` to proceed.")
    else:
        print(f"ACTION: Await or submit more expert responses. Minimum {target_experts} required.")

def advance_to_review():
    state = load_state()
    if state["phase"] != "EXPERT_PHASE":
        print(f"ERROR: Cannot advance from {state['phase']}.")
        sys.exit(1)
        
    target_experts = state.get("num_experts", 5)
    if len(state["experts"]) < target_experts:
        print(f"ERROR: Minimum {target_experts} experts required to advance.")
        sys.exit(1)
    
    state["phase"] = "REVIEW_PHASE"
    save_state(state)
    print("STATE: REVIEW_PHASE")
    print("ACTION: The expert critiques are complete. Run `pixi run python storm_referee.py get_review_payload` to retrieve the anonymized text.")
    print(f"ACTION: Use `invoke_subagent` to spawn {target_experts} Reviewer subagents, passing them the anonymized text. Ask them to identify the strongest point, the clashes, and what was missed in under 200 words.")
    print("MANDATORY TOOL CONSTRAINT: During this phase, you are ONLY allowed to use the 'invoke_subagent' tool, and 'run_command' or 'write_to_file' to submit responses. You are strictly forbidden from taking action on the project files.")
    print(f"MANDATORY HALT: Stop and yield execution until all {target_experts} Reviewer subagents have replied.")

def get_review_payload():
    state = load_state()
    if state["phase"] != "REVIEW_PHASE":
        print(f"ERROR: Cannot get review payload in phase {state['phase']}.")
        sys.exit(1)
    
    payload = f"Proposal: {state['proposal']}\n\nExpert Critiques:\n"
    for i, (persona, response) in enumerate(state["experts"].items()):
        payload += f"--- Response {chr(65+i)} ---\n{response}\n\n"
    print(payload)

def submit_review(reviewer_id, response):
    state = load_state()
    if state["phase"] != "REVIEW_PHASE":
        print(f"ERROR: Expected state REVIEW_PHASE, but currently in {state['phase']}.")
        sys.exit(1)
    
    validate_response(response)
    
    state["reviews"][reviewer_id] = response
    save_state(state)
    
    target_experts = state.get("num_experts", 5)
    num_reviews = len(state["reviews"])
    print(f"SUCCESS: Recorded review '{reviewer_id}'. Total reviews: {num_reviews}/{target_experts}.")
    
    if num_reviews >= target_experts:
        state["phase"] = "CHAIRMAN_PHASE"
        save_state(state)
        print("STATE: CHAIRMAN_PHASE")
        print("ACTION: The peer reviews are complete. Run `pixi run python storm_referee.py get_synthesis_payload` to retrieve all raw data.")
        print("ACTION: Synthesize the final verdict in Markdown format.")
        print("MANDATORY TOOL CONSTRAINT: During this phase, you are ONLY allowed to use the 'write_to_file' tool to write the final artifact, and 'run_command' for referee interactions. No other actions allowed.")
    else:
        print(f"ACTION: Await or submit more reviewer responses. Minimum {target_experts} required.")

def get_synthesis_payload():
    state = load_state()
    if state["phase"] != "CHAIRMAN_PHASE":
        print(f"ERROR: Cannot get synthesis payload in phase {state['phase']}.")
        sys.exit(1)
    
    payload = f"Proposal: {state['proposal']}\n\n=== EXPERT CRITIQUES ===\n"
    for persona, response in state["experts"].items():
        payload += f"--- {persona} ---\n{response}\n\n"
        
    payload += "=== PEER REVIEWS ===\n"
    for reviewer_id, response in state["reviews"].items():
        payload += f"--- Reviewer {reviewer_id} ---\n{response}\n\n"
        
    print(payload)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STORM Council Referee")
    subparsers = parser.add_subparsers(dest="command")
    
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("proposal", type=str)
    init_parser.add_argument("--num_experts", type=int, default=5)
    
    expert_parser = subparsers.add_parser("submit_expert")
    expert_parser.add_argument("--persona", type=str, required=True)
    expert_parser.add_argument("--response", type=str, required=True)
    
    subparsers.add_parser("advance_to_review")
    subparsers.add_parser("get_review_payload")
    
    review_parser = subparsers.add_parser("submit_review")
    review_parser.add_argument("--reviewer_id", type=str, required=True)
    review_parser.add_argument("--response", type=str, required=True)
    
    subparsers.add_parser("get_synthesis_payload")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init(args.proposal, args.num_experts)
    elif args.command == "submit_expert":
        submit_expert(args.persona, args.response)
    elif args.command == "advance_to_review":
        advance_to_review()
    elif args.command == "get_review_payload":
        get_review_payload()
    elif args.command == "submit_review":
        submit_review(args.reviewer_id, args.response)
    elif args.command == "get_synthesis_payload":
        get_synthesis_payload()
    else:
        parser.print_help()
