# Static Generator

A small learning project for building HTML nodes (`HTMLNode`, `LeafNode`, `ParentNode`) and inline text nodes (`TextNode`), then generating a static site into the `docs/` folder.

## Requirements

- Python 3.10+

## Run (local)

    python3 src/main.py
    ./main.sh

This builds into `docs/` and serves it on port `8888`.

## Build for GitHub Pages

    ./build.sh

This runs `python3 src/main.py "/static_generator/"` to set the base path for GitHub Pages. Replace `/static_generator/` with your repo name if needed.

## Tests

    python3 -m unittest discover -s src
    ./test.sh

## Project layout

- `src/htmlnode.py`: `HTMLNode`, `LeafNode`, `ParentNode`
- `src/textnode.py`: `TextType`, `TextNode`, `text_node_to_html_node`
- `src/markdown.py`: markdown parsing and HTML conversion
- `src/main.py`: build entry point
- `src/test_htmlnode.py`, `src/test_textnode.py`: unit tests
