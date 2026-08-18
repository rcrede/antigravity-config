#!/usr/bin/env python3
"""MapWeaver: Lightweight YAML-frontmatter Obsidian Vault indexer."""

import argparse
import os
from pathlib import Path

def parse_yaml_frontmatter(content):
    """Extract specific YAML keys from markdown frontmatter without external dependencies."""
    lines = content.splitlines()
    if not lines or not lines[0].strip() == "---":
        return None
        
    metadata = {}
    in_list = False
    current_key = None
    
    for line in lines[1:]:
        if line.strip() == "---":
            break
            
        stripped = line.strip()
        if not stripped:
            continue
            
        if line.startswith(" ") or line.startswith("\t"):
            # Continuation or list item
            if current_key and stripped.startswith("- "):
                val = stripped[2:].strip().strip("'\"")
                if current_key not in metadata:
                    metadata[current_key] = []
                elif not isinstance(metadata[current_key], list):
                    metadata[current_key] = [metadata[current_key]]
                metadata[current_key].append(val)
        else:
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                
                if val:
                    # check if val starts with [ and ends with ]
                    if val.startswith("[") and val.endswith("]"):
                        items = [x.strip().strip("'\"") for x in val[1:-1].split(",")]
                        metadata[key] = [x for x in items if x]
                    else:
                        metadata[key] = val
                else:
                    current_key = key
                    metadata[key] = []

    return metadata

def extract_metadata(file_path):
    """Extract specific YAML keys from a markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        frontmatter = parse_yaml_frontmatter(content)
        if not frontmatter:
            return None
            
        return {
            "type": frontmatter.get("type"),
            "description": frontmatter.get("description") or frontmatter.get("summary"),
            "status": frontmatter.get("status"),
            "tags": frontmatter.get("tags"),
            "aliases": frontmatter.get("aliases")
        }
    except Exception:
        return None

def format_metadata(metadata):
    """Format metadata for display in the index."""
    if not metadata:
        return ""
    
    parts = []
    if metadata.get("type"):
        parts.append(f"**Type:** {metadata['type']}")
    if metadata.get("status"):
        parts.append(f"**Status:** {metadata['status']}")
    if metadata.get("tags"):
        tags = metadata["tags"]
        if isinstance(tags, list):
            tags = ", ".join([str(t) for t in tags])
        parts.append(f"**Tags:** {tags}")
    if metadata.get("aliases"):
        aliases = metadata["aliases"]
        if isinstance(aliases, list):
            aliases = ", ".join([str(a) for a in aliases])
        parts.append(f"**Aliases:** {aliases}")
    if metadata.get("description"):
        parts.append(f"**Desc:** {metadata['description']}")
        
    if not parts:
        return ""
    return " — " + " | ".join(parts)

def build_vault_index(root_dir):
    root = Path(root_dir).resolve()
    
    # 1. Generate ONE root .CODEMAP.md mapping the top-level directories
    top_level_dirs = []
    for item in root.iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name not in ["node_modules", "venv", "__pycache__"]:
            top_level_dirs.append(item)
            
    top_level_dirs.sort(key=lambda x: x.name)
    
    root_codemap_lines = ["# Vault Map", ""]
    root_codemap_lines.append("## Top-Level Directories")
    for d in top_level_dirs:
        root_codemap_lines.append(f"- [[{d.name}/_Index|{d.name}]]")
        
    root_codemap_path = root / ".CODEMAP.md"
    root_codemap_path.write_text("\n".join(root_codemap_lines) + "\n", encoding="utf-8")
    print(f"Generated {root_codemap_path}")
    
    # 2. Generate ONE _Index.md inside each top-level directory
    for d in top_level_dirs:
        index_lines = [f"# Index of {d.name}", ""]
        
        md_files = list(d.rglob("*.md"))
        md_files = [f for f in md_files if f.name not in ["_Index.md", ".CODEMAP.md"]]
        md_files.sort(key=lambda x: str(x.relative_to(d)))
        
        if md_files:
            index_lines.append("## Files")
            for f in md_files:
                metadata = extract_metadata(f)
                meta_str = format_metadata(metadata)
                
                # Use standard obsidian wikilink format.
                if meta_str:
                    index_lines.append(f"- [[{f.stem}]] {meta_str}")
                else:
                    index_lines.append(f"- [[{f.stem}]]")
                
        index_path = d / "_Index.md"
        index_path.write_text("\n".join(index_lines) + "\n", encoding="utf-8")
        print(f"Generated {index_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MapWeaver: Lightweight YAML-frontmatter Obsidian Vault indexer.")
    parser.add_argument("--build", type=str, metavar="DIR", help="Target vault root directory to index")
    
    args = parser.parse_args()
    if args.build:
        build_vault_index(args.build)
    else:
        parser.print_help()
