import re
from html_node import HTMLNode, ParentNode, LeafNode
from text_node import text_node_to_html_node
from inline_markdown.inline_parser import text_to_textnodes


def detect_heading(block: str) -> bool:
    return re.match(r"^\s*#{1,6}\s+", block) is not None


def convert_heading(block: str) -> HTMLNode:
    match = re.match(r"^\s*(#{1,6})\s+(.*)", block)
    if match:
        heading_number = len(match.group(1))
        tag = f"h{heading_number}"
        content = match.group(2).strip()
        children_text = text_to_textnodes(content)
        children = [
            text_node_to_html_node(text_node)
            for text_node in children_text
            if text_node.text.strip()
        ]
        return ParentNode(tag=tag, children=children)
    return ParentNode(
        tag="h1", children=[LeafNode(tag="text", value=block)]
    )  # Fallback


def detect_code(block: str) -> bool:
    lines = block.split("\n")
    return len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```")


def convert_code(block: str) -> HTMLNode:
    code_content = "\n".join(block.split("\n")[1:-1])
    return ParentNode(tag="pre", children=[LeafNode(tag="code", value=code_content)])


def detect_quote(block: str) -> bool:
    return all(line.lstrip().startswith(">") for line in block.split("\n"))


def convert_quote(block: str) -> HTMLNode:
    lines = block.split("\n")
    lines = [line[1:].strip() for line in lines]
    block_content = "\n".join(lines)
    children_text = text_to_textnodes(block_content)
    children = [
        text_node_to_html_node(text_node)
        for text_node in children_text
        if text_node.text.strip()
    ]
    return ParentNode(tag="blockquote", children=children)


def detect_unordered_list(block: str) -> bool:
    return all(line.lstrip().startswith(("* ", "- ")) for line in block.split("\n"))


def convert_unordered_list(block: str) -> HTMLNode:
    items = []
    for line in block.split("\n"):
        list_item_content = line[2:].strip()
        children_text = text_to_textnodes(list_item_content)
        children = [
            text_node_to_html_node(text_node)
            for text_node in children_text
            if text_node.text.strip()
        ]
        items.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ul", children=items)


def detect_ordered_list(block: str) -> bool:
    return all(re.match(r"^\d+\.\s+", line) for line in block.split("\n"))


def convert_ordered_list(block: str) -> HTMLNode:
    items = []
    for line in block.split("\n"):
        list_item_content = line[line.index(". ") + 2 :].strip()
        children_text = text_to_textnodes(list_item_content)
        children = [
            text_node_to_html_node(text_node)
            for text_node in children_text
            if text_node.text.strip()
        ]
        items.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ol", children=items)


def detect_paragraph(block: str) -> bool:
    return False


def convert_paragraph(block: str) -> HTMLNode:
    children_text = text_to_textnodes(block)
    children = [
        text_node_to_html_node(text_node)
        for text_node in children_text
        if text_node.text.strip()
    ]
    return ParentNode(tag="p", children=children)
