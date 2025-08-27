#!/bin/bash
# $1: notes_path (не используется в этой заглушке)
# $2: cache_file

NOTES_PATH=$1
CACHE_FILE=$2

# Имитация сканирования и создания JSON
echo '{
  "nodes": [
    {"id": "note1.md", "label": "Заметка 1", "path": "/home/sergey/Documents/Notes/note1.md"},
    {"id": "note2.org", "label": "Заметка 2", "path": "/home/sergey/Documents/Notes/note2.org"},
    {"id": "project_idea.md", "label": "Идея проекта", "path": "/home/sergey/Documents/Notes/project_idea.md"}
  ],
  "edges": [
    {"from": "note1.md", "to": "note2.org"},
    {"from": "note1.md", "to": "project_idea.md"}
  ]
}' > "$CACHE_FILE"

exit 0
