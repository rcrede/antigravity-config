#!/usr/bin/env python3
import json
import os
import argparse
import yaml

import re

def create_dsln(json_path, output_dir, zettel_dir, scope_tag):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    title = data.get('title', 'Untitled_Paper')
    safe_title = re.sub(r'[\\/*?:"<>|]', '_', title).replace(' ', '_')
    dsln_path = os.path.join(output_dir, f"{safe_title}.md")
    
    # Write DSLN
    clean_scope = scope_tag.lstrip('#')
    frontmatter = {
        'tags': [clean_scope],
        'ara_data': data
    }
    
    os.makedirs(output_dir, exist_ok=True)
    with open(dsln_path, 'w') as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, default_flow_style=False)
        f.write("---\n\n")
        f.write(f"# {title}\n\n")
        f.write("<!-- Agent will fill dense summary here -->\n")
        
    print(f"Created DSLN: {dsln_path}")
    
    # Write Zettels
    os.makedirs(zettel_dir, exist_ok=True)
    concepts_data = data.get('concepts') or []
    methods_data = data.get('methods') or []
    concepts = concepts_data + methods_data
    for concept in concepts:
        c_name = concept.get('name', 'Unknown_Concept')
        safe_c_name = re.sub(r'[\\/*?:"<>|]', '_', c_name).replace(' ', '_')
        z_path = os.path.join(zettel_dir, f"{safe_c_name}.md")
        
        # Strip '#' from tags for clean frontmatter
        clean_scope = scope_tag.lstrip('#')
        z_frontmatter = {
            'tags': ['zettel/unreviewed', clean_scope, 'zettel/concept']
        }
        
        with open(z_path, 'w') as f:
            f.write("---\n")
            yaml.dump(z_frontmatter, f, default_flow_style=False)
            f.write("---\n\n")
            f.write(f"# {c_name}\n\n")
            f.write(f"Source: [[{safe_title}]]\n\n")
            f.write(f"Description: {concept.get('description', '')}\n")
            
        print(f"Created Zettel: {z_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", help="Path to the JSON file containing extracted ARA data")
    parser.add_argument("dsln_dir", help="Output directory for DSLN")
    parser.add_argument("zettel_dir", help="Output directory for Zettels")
    parser.add_argument("scope_tag", help="Scope tag (e.g. #project/so3lr)")
    args = parser.parse_args()
    
    create_dsln(args.json_file, args.dsln_dir, args.zettel_dir, args.scope_tag)
