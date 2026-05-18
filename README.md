# MD -> HTML

A hand-rolled static site generator written in Python. No frameworks, no dependencies — just Markdown in, HTML out.

---

## How it works

- Markdown files in `content/` are parsed and injected into `template.html`
- Static assets (CSS, images) from `static/` are copied to the output directory
- Nav and asset links are rewritten with the correct basepath for the target environment

## Requirements

- Python 3.10+

---

## Local development

```bash
./main.sh
```

Builds to `public/` (gitignored) and serves on `http://localhost:8888`.  
**Does not touch `docs/`** — safe to run anytime.

## Deploy to GitHub Pages

```bash
./build.sh
git add docs/
git commit -m "rebuild"
git push
```

Builds to `docs/` with the `/saksham_portfolio/` basepath, then push to deploy.  
GitHub Pages serves from the `docs/` folder on the `main` branch.

> ⚠️ Never run `python3 src/main.py` without arguments and commit `docs/` — it will use the wrong basepath and break the live site.

---

## Project layout

```
.
├── content/          # Markdown source pages
│   ├── index.md
│   ├── about/
│   ├── projects/
│   └── contact/
├── static/           # Assets copied as-is to output
│   └── index.css
├── src/
│   ├── main.py       # Build entry point
│   ├── markdown.py   # Markdown parser and HTML converter
│   ├── htmlnode.py   # HTMLNode, LeafNode, ParentNode
│   ├── textnode.py   # TextNode and inline text parsing
│   └── Static_to_public.py
├── template.html     # Page shell (title + nav + content slot)
├── docs/             # GitHub Pages output (built by build.sh)
├── public/           # Local dev output (built by main.sh, gitignored)
├── main.sh           # Local dev: builds to public/ + serves on :8888
├── build.sh          # GitHub Pages: builds to docs/ with correct basepath
└── test.sh           # Runs unit tests
```

## Tests

```bash
./test.sh
# or
python3 -m unittest discover -s src
```
