import os
import sys

from markdown import extract_title, markdown_to_html_node
from Static_to_public import static_to_public


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if not basepath.startswith("/"):
        basepath = f"/{basepath}"
    if not basepath.endswith("/"):
        basepath = f"{basepath}/"

    source = "static"
    destination = sys.argv[2] if len(sys.argv) > 2 else "docs"
    static_to_public(source, destination)
    generate_pages_recursive("content", "template.html", destination, basepath)


def generate_page(from_path, template_path, dest_path, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        var1 = file.read()

    with open(template_path, "r") as file:
        var2 = file.read()

    html_content = markdown_to_html_node(var1).to_html()
    title = extract_title(var1)

    var2 = var2.replace("{{ Title }}", title)
    var2 = var2.replace("{{ Content }}", html_content)
    var2 = var2.replace('href="/', f'href="{basepath}')
    var2 = var2.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(var2)


def generate_pages_recursive(
    dir_path_content: str,
    template_path: str,
    dest_dir_path: str,
    basepath: str,
) -> None:
    for entry in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(content_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(content_path, template_path, dest_path, basepath)
        elif entry.endswith(".md"):
            html_name = f"{os.path.splitext(entry)[0]}.html"
            dest_html_path = os.path.join(dest_dir_path, html_name)
            generate_page(content_path, template_path, dest_html_path, basepath)


if __name__ == "__main__":
    main()
