# MD -> HTML

A hand-rolled static site generator written in Python. No frameworks, no dependencies —> just Markdown in, HTML out.

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
git add .
git commit -m "rebuild"
git push
```

Builds to `docs/` with the `/saksham_portfolio/` basepath, then push to deploy.  
GitHub Pages serves from the `docs/` folder on the `main` branch.

> Never run `python3 src/main.py` without arguments and commit `docs/` — it will use the wrong basepath and break the live site.

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

**Files & Functions**

- **`src/main.py`**:
	- **Key functions:** `main()`, `generate_page(from_path, template_path, dest_path, basepath)`, `generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath)`.
	- **Takes:** command-line args or paths to content/template/destination and a `basepath` string.
	- **Returns:** writes HTML files to the destination (no return value).
	- **Example:** `generate_page("content/index.md", "template.html", "public/index.html", "/")` — reads `content/index.md`, converts it to HTML, injects into `template.html`, and writes `public/index.html`.

- **`src/markdown.py`**:
	- **Key functions:** `markdown_to_blocks(markdown) -> list[str]`, `block_to_block_type(block) -> BlockType`, `markdown_to_html_node(markdown) -> ParentNode`, `extract_title(markdown) -> str`.
	- **Takes:** a Markdown `str`.
	- **Returns:** parsed blocks, HTML node tree (`ParentNode`) and extracted title string.
	- **Example:** `node = markdown_to_html_node("# Hello\nThis is text")` — returns a `ParentNode('div', [...])`; `extract_title("# Hello\n...")` -> `'Hello'`.

- **`src/htmlnode.py`**:
	- **Key classes / methods:** `HTMLNode`, `LeafNode(tag, value)`, `ParentNode(tag, children)`, `to_html()`.
	- **Takes:** node tag, value or children and optional props.
	- **Returns:** `to_html()` produces an HTML `str` for that node subtree.
	- **Example:** `ParentNode('p', [LeafNode(None, 'text')]).to_html()` -> `"<p>text</p>"`.

- **`src/textnode.py`**:
	- **Key classes / functions:** `TextNode(text, TextType, url=None)`, `text_node_to_html_node(text_node) -> LeafNode`, `text_to_textnodes(text) -> list[TextNode]` and helpers for links/images/formatting.
	- **Takes:** plain text `str` (possibly containing inline markdown like `**bold**`, `*italic*`, `` `code` ``, `[link](url)`, `![alt](src)`).
	- **Returns:** a list of `TextNode`s or `LeafNode`s suitable for `HTMLNode` children.
	- **Example:** `text_to_textnodes("This is **bold**")` -> `[TextNode("This is ", TEXT), TextNode("bold", BOLD)]` and `text_node_to_html_node(...)` -> `<b>bold</b>`.

- **`src/Static_to_public.py`**:
	- **Key function:** `static_to_public(start_path: str, final_path: str)`.
	- **Takes:** source static directory and destination directory paths.
	- **Returns:** copies the static tree into the destination (no return value).
	- **Example:** `static_to_public('static', 'public')` — copies `static/` to `public/` (removes `public/` first if it exists).

- **`template.html`**:
	- **Role:** page shell with placeholders `{{ Title }}` and `{{ Content }}` and standard asset links.
	- **Takes:** injected title and HTML content strings (via `src/main.py` flow).
	- **Example:** template placeholder replacement yields a final HTML page with inserted title and content.

- **Shell scripts:**
	- **`main.sh`**: builds to `public/` and serves locally (dev).
	- **`build.sh`**: builds to `docs/` with the GitHub Pages basepath.
	- **`test.sh`**: runs unit tests.

These notes map the repository files to their main responsibilities and show a simple example usage for each conversion step.


**How the build works**

- **Entry point:** `src/main.py` ([src/main.py](src/main.py#L1)). When you run `./main.sh` or `./build.sh` it ultimately calls the code in this module.

- **Full flow (step-by-step):**
	1. Determine `basepath` and `destination` (from command-line args) — the `basepath` ensures links work when the site is hosted under a subpath (important for GitHub Pages).
	2. Copy static assets: `static_to_public('static', destination)` — implemented in [src/Static_to_public.py](src/Static_to_public.py#L1).
	3. Walk `content/` recursively with `generate_pages_recursive(...)` — for each `*.md` file it calls `generate_page(...)` to build an HTML file in the destination.
	4. For each page, `generate_page(from_path, template_path, dest_path, basepath)` does:
		 - Read the markdown source and the `template.html` file.
		 - Convert markdown -> HTML node tree via `markdown_to_html_node(markdown)` (see [src/markdown.py](src/markdown.py#L1)).
		 - Call `.to_html()` on the root node to obtain an HTML string (nodes are defined in [src/htmlnode.py](src/htmlnode.py#L1)).
		 - Extract page title with `extract_title(markdown)`.
		 - Replace `{{ Title }}` and `{{ Content }}` placeholders in the template with the extracted title and converted content.
		 - Rewrite absolute `href` and `src` prefixes (`"/"`) to include `basepath` so links point correctly when hosted under a subpath.
		 - Write the resulting HTML to the destination path (creating directories as needed).

- **Markdown parsing internals:**
	- `src/markdown.py` splits markdown into block-level elements and turns each block into an `HTMLNode` subtree. Inline formatting (bold, italic, links, images, code) is parsed by `src/textnode.py` into `TextNode`s which are converted into `LeafNode`s (or elements with props) by `text_node_to_html_node`.
	- The final `ParentNode(...).to_html()` call (from [src/htmlnode.py](src/htmlnode.py#L1)) serializes the node tree into a single HTML string.

- **Why asset rewriting / basepath matters:**
	- Locally (`./main.sh`) the site is served from `/` (so `href="/index.html"` works). On GitHub Pages the site is often hosted at `/username_repo/` — linking from `/` would break.
	- `build.sh` sets the correct `basepath` (e.g. `/saksham_portfolio/`) and writes output into `docs/`. GitHub Pages serves the repository pages from the `docs/` folder on the `main` branch, so committing `docs/` publishes the site at your repo's Pages URL.

- **Concrete examples**
	- Build programmatically (same as `main.sh` does):

```python
from src.main import generate_page
generate_page("content/index.md", "template.html", "public/index.html", "/")
```

	- Local dev quick run:

```bash
./main.sh
# -> builds to public/ and serves at http://localhost:8888
```

	- Build for GitHub Pages:

```bash
./build.sh
git add . 
git commit -m "rebuild"
git push
# -> docs/ contains the site with links rewritten to the repo basepath
```


## Tests

```bash
./test.sh
# or
python3 -m unittest discover -s src
```

