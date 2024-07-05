import re
from typing import List

from text_node import TextNode, TextType

from .inline_types import InlineDelimiters


def text_type_delimiter_map(delimiter: str) -> InlineDelimiters:
    for dtype in InlineDelimiters:
        if isinstance(dtype.value, tuple):
            if delimiter in dtype.value:
                return dtype
        else:
            if delimiter == dtype.value:
                return dtype
    raise ValueError(f"Delimiter '{delimiter}' not found in InlineDelimiters")


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter_str: str
) -> List[TextNode]:
    new_nodes = []

    for node in old_nodes:
        try:
            text_type = TextType[node.text_type.upper()]
        except KeyError:
            raise ValueError("Invalid Text Type")

        if text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        delimiters = text_type_delimiter_map(delimiter_str)
        added_to_new_nodes = False

        for delimiter in delimiters.value:
            if delimiter in node.text:
                nodes = split_nodes_recursively(
                    node.text, delimiter, TextType[delimiters.name]
                )
                for n in nodes:
                    if n.text.strip():
                        new_nodes.append(n)
                added_to_new_nodes = True
                break

        if not added_to_new_nodes and node.text.strip():
            new_nodes.append(node)

    return new_nodes


def split_nodes_recursively(
    text: str, delimiter: str, text_type: TextType
) -> List[TextNode]:
    parts = []
    start = 0

    while start < len(text):
        first_pos = text.find(delimiter, start)
        if first_pos == -1:
            break

        prefix = text[start:first_pos]
        parts.append(TextNode(prefix, TextType.TEXT.value))

        start = first_pos + len(delimiter)

        second_pos = text.find(delimiter, start)

        if second_pos == -1:
            continue

        middle = text[start:second_pos]
        parts.append(TextNode(middle, text_type.value))

        start = second_pos + len(delimiter)

    suffix = text[start:]
    parts.append(TextNode(suffix, TextType.TEXT.value))

    parts = [part for part in parts if part.text.strip()]

    return parts


def extract_markdown_image(text: str) -> List[(str)]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_link(text: str) -> List[(str)]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type.lower() == "text":
            images = extract_markdown_image(node.text)
            if images:
                remaining_text = node.text
                for image in images:
                    start, _, end = remaining_text.partition(
                        f"![{image[0]}]({image[1]})"
                    )
                    if start.strip():
                        new_nodes.append(TextNode(start, "text"))
                    new_nodes.append(TextNode(image[0], "image", image[1]))
                    remaining_text = end
                if remaining_text.strip():
                    new_nodes.append(TextNode(remaining_text, "text"))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)

    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type.lower() == "text":
            links = extract_markdown_link(node.text)
            if links:
                remaining_text = node.text
                for link in links:
                    start, _, end = remaining_text.partition(f"[{link[0]}]({link[1]})")
                    if start.strip():
                        new_nodes.append(TextNode(start, "text"))
                    new_nodes.append(TextNode(link[0], "link", url=link[1]))
                    remaining_text = end
                if remaining_text.strip():
                    new_nodes.append(TextNode(remaining_text, "text"))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)

    return new_nodes
