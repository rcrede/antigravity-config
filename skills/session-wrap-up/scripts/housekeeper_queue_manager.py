import json
import os
import sys
import argparse

# The script runs from the skill script folder, so we need to locate the vault root.
# Usually the vault root is /home/rcrede/Documents/Obsidian Vault. We can check via env or hardcode, 
# but better to infer from known structure or take as arg.
VAULT_DIR = os.environ.get("OBSIDIAN_VAULT_DIR", "/home/rcrede/Documents/Obsidian Vault")
QUEUE_FILE = os.path.join(VAULT_DIR, "00_Inbox", "Semantic_Drift_Queue.json")

def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_queue(queue):
    os.makedirs(os.path.dirname(QUEUE_FILE), exist_ok=True)
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)

def list_queue():
    queue = load_queue()
    if not queue:
        print("Semantic Drift Queue is empty.")
        return
    
    print(f"--- {len(queue)} items in Semantic Drift Queue ---")
    for idx, item in enumerate(queue):
        print(f"[{idx}] Modified Zettel: {item.get('modified_zettel')}")
        print(f"    Affected Page: {item.get('affected_page')}")
        print(f"    Timestamp: {item.get('timestamp')}")
        print("-" * 40)

def resolve_item(index):
    queue = load_queue()
    if index < 0 or index >= len(queue):
        print(f"Error: Invalid index {index}", file=sys.stderr)
        sys.exit(1)
        
    resolved = queue.pop(index)
    save_queue(queue)
    print(f"Successfully resolved and removed index {index}: {resolved.get('affected_page')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage the Semantic Drift Queue safely.")
    subparsers = parser.add_subparsers(dest="command")
    
    list_parser = subparsers.add_parser("list", help="List all items in the queue")
    
    resolve_parser = subparsers.add_parser("resolve", help="Remove an item from the queue after processing")
    resolve_parser.add_argument("index", type=int, help="Index of the item to resolve")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_queue()
    elif args.command == "resolve":
        resolve_item(args.index)
    else:
        parser.print_help()
