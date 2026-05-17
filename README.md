# Static Generator

A small learning project for building HTML nodes (`HTMLNode`, `LeafNode`, `ParentNode`) and inline text nodes (`TextNode`).

## Requirements

- Python 3.10+

## Run

    python3 src/main.py
    ./main.sh

## Tests

    python3 -m unittest discover -s src
    ./test.sh

## Project layout

- `src/htmlnode.py`: `HTMLNode`, `LeafNode`, `ParentNode`
- `src/textnode.py`: `TextType`, `TextNode`, `text_node_to_html_node`
- `src/main.py`: demo entry point
- `src/test_htmlnode.py`, `src/test_textnode.py`: unit tests
