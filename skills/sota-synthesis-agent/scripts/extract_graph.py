#!/usr/bin/env python3
import os
import json
import argparse
import glob

def parse_frontmatter(content):
    if not content.startswith("---"):
        return None, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content
    import yaml
    try:
        frontmatter = yaml.safe_load(parts[1])
        return frontmatter, parts[2]
    except Exception:
        return None, content

def extract_graph(vault_dir, scope_tag):
    graph = {
        "dslns": [],
        "zettels": []
    }
    
    for root, _, files in os.walk(vault_dir):
        for file in files:
            if not file.endswith('.md'):
                continue
                
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
                
            frontmatter, body = parse_frontmatter(content)
            if not frontmatter:
                continue
                
            tags = frontmatter.get('tags', [])
            if isinstance(tags, str):
                tags = [tags]
            
            # Normalize tags (remove leading '#')
            normalized_tags = [t.lstrip('#') for t in tags]
            normalized_scope = scope_tag.lstrip('#')
                
            if normalized_scope not in normalized_tags:
                continue
                
            if 'zettel/unreviewed' in normalized_tags:
                continue
                
            # Is it a DSLN?
            if 'ara_data' in frontmatter:
                graph["dslns"].append({
                    "title": file.replace('.md', ''),
                    "path": filepath,
                    "ara_data": frontmatter['ara_data']
                })
            else:
                graph["zettels"].append({
                    "title": file.replace('.md', ''),
                    "path": filepath,
                    "tags": tags,
                    "content": body.strip()
                })
                
    return graph

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("vault_dir", help="Path to the Obsidian Vault")
    parser.add_argument("scope_tag", help="Tag to filter by (e.g. #project/so3lr)")
    args = parser.parse_args()
    
    # We require pyyaml but it should be available in the environment running this, 
    # or the agent can install it if needed.
    graph = extract_graph(args.vault_dir, args.scope_tag)
    print(json.dumps(graph, indent=2))
