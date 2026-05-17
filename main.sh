#!/bin/bash
# Local dev only — builds to public/ so docs/ (GitHub Pages) is never touched
python3 src/main.py / public
cd public && python3 -m http.server 8888
