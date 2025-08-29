import os
import sys
import json
import re

def create_graph_from_path(notes_path, ignore_patterns=None):
    """Scans a directory for .md and .org files, extracts nodes and simple edges."""
    if ignore_patterns is None:
        ignore_patterns = []
    
    nodes = []
    edges = []
    file_paths = {}

    # First pass: Collect all valid note files and create nodes
    for root, dirs, files in os.walk(notes_path):
        # Exclude directories based on ignore patterns
        dirs[:] = [d for d in dirs if d not in ignore_patterns]
        
        for file in files:
            if file.endswith(('.md', '.org')) and file not in ignore_patterns:
                full_path = os.path.join(root, file)
                node_id = os.path.basename(full_path) # Use filename as ID for simplicity
                node_label = os.path.splitext(node_id)[0]
                
                nodes.append({
                    "id": node_id,
                    "label": node_label,
                    "path": os.path.abspath(full_path)
                })
                file_paths[node_id.lower()] = full_path # Store for quick lookup (case-insensitive)

    # Second pass: Scan file contents for links and create edges
    for node in nodes:
        try:
            with open(node['path'], 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple regex to find [[link]] or [[link.ext]]
                # This will need to be more robust for full Org/Markdown parsing
                links = re.findall(r'\[\[([^\]]+?)(?:\.md|\.org)?\]\]', content)
                
                for link_target in links:
                    # Try to find the target file by its name (case-insensitive)
                    target_node_id = None
                    if link_target.lower() + '.md' in file_paths:
                        target_node_id = link_target.lower() + '.md'
                    elif link_target.lower() + '.org' in file_paths:
                        target_node_id = link_target.lower() + '.org'
                    elif link_target.lower() in file_paths: # If link is just filename without extension
                        target_node_id = link_target.lower()
                    
                    # If a valid target node is found, add an edge
                    if target_node_id and node['id'].lower() != target_node_id:
                        edges.append({"from": node['id'], "to": target_node_id})
        except Exception as e:
            print(f"Warning: Could not read file {node['path']} for link parsing: {e}")

    return {"nodes": nodes, "edges": edges}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <notes_path> <cache_file> [ignore_patterns...]")
        sys.exit(1)

    notes_path = sys.argv[1]
    cache_file = sys.argv[2]
    ignore_patterns = sys.argv[3:] if len(sys.argv) > 3 else []

    if not os.path.isdir(notes_path):
        print(f"Notes directory {notes_path} not found. Creating it.")
        os.makedirs(notes_path)

    print(f"Scanning for notes in: {notes_path}")
    if ignore_patterns:
        print(f"Ignoring: {ignore_patterns}")
    graph_data = create_graph_from_path(notes_path, ignore_patterns)

    try:
        with open(cache_file, 'w') as f:
            json.dump(graph_data, f, indent=2)
        print(f"Successfully wrote graph data to {cache_file}")
    except Exception as e:
        print(f"Error writing to cache file: {e}")
        sys.exit(1)

    sys.exit(0)
