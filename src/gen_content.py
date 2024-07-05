from pathlib import Path
from block_markdown.block_markdown import markdown_to_html_nodes
import logging

logging.basicConfig(level=logging.INFO)


def generate_pages_recursively(
    dir_path_content: Path, template_path: Path, dest_dir_path: Path
) -> None:
    logging.info(f"Generating pages from {dir_path_content} to {dest_dir_path}")

    for item in dir_path_content.iterdir():
        dest_path = dest_dir_path / item.name
        if item.is_file():
            dest_path = dest_path.with_suffix(".html")
            generate_page(item, template_path, dest_path)
        else:
            generate_pages_recursively(item, template_path, dest_path)


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    logging.info(f"Generating page: {from_path} -> {dest_path}")

    markdown_content = read_file(from_path)
    template = read_file(template_path)

    node = markdown_to_html_nodes(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    filled_template = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html
    )

    if not dest_path.parent.exists():
        dest_path.parent.mkdir(parents=True, exist_ok=True)

    write_file(dest_path, filled_template)


def read_file(path: Path) -> str:
    with path.open("r", encoding="utf-8") as file:
        return file.read()


def write_file(path: Path, content: str):
    with path.open("w", encoding="utf-8") as file:
        file.write(content)


def extract_title(md: str) -> str:
    for line in md.split("\n"):
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")
