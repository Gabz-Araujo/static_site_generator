import re
from enum import Enum
from typing import List

from html_node import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from text_node import text_node_to_html_node


class BlockDelimiters(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> List[str]:
    markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")
    blocks = markdown.split("\n\n")

    cleaned_blocks = []
    for block in blocks:
        cleaned_block_lines = [line.strip() for line in block.split("\n")]
        cleaned_block = "\n".join(cleaned_block_lines)
        cleaned_blocks.append(cleaned_block.strip())

    cleaned_blocks = [block for block in cleaned_blocks if block]
    return cleaned_blocks


def block_to_block_type(block: str) -> BlockDelimiters:
    lines = block.split("\n")

    if block.startswith("#"):
        first_part = block.split(" ")[0]
        count_hash = first_part.count("#")
        if 0 < count_hash <= 6 and all(c == "#" for c in first_part):
            return BlockDelimiters.HEADING

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockDelimiters.CODE

    if block.startswith(">"):
        if all(line.startswith(">") for line in lines):
            return BlockDelimiters.QUOTE
        return BlockDelimiters.PARAGRAPH

    if block.startswith("* "):
        if all(line.startswith("* ") for line in lines):
            return BlockDelimiters.UNORDERED_LIST
        return BlockDelimiters.PARAGRAPH

    if block.startswith("- "):
        if all(line.startswith("- ") for line in lines):
            return BlockDelimiters.UNORDERED_LIST
        return BlockDelimiters.PARAGRAPH

    if block.startswith("1. "):
        for i, line in enumerate(lines, 1):
            if not line.startswith(f"{i}. "):
                return BlockDelimiters.PARAGRAPH
        return BlockDelimiters.ORDERED_LIST

    return BlockDelimiters.PARAGRAPH


def block_to_html_nodes(block: str, block_type: BlockDelimiters) -> HTMLNode:
    if block_type == BlockDelimiters.PARAGRAPH:
        children_text = text_to_textnodes(block)
        children = [
            text_node_to_html_node(text_node)
            for text_node in children_text
            if text_node.text.strip()
        ]
        return ParentNode(tag="p", children=children)

    if block_type == BlockDelimiters.HEADING:
        heading_number = block.count("#")
        tag = f"h{heading_number}"
        content = block[heading_number:].strip()
        children_text = text_to_textnodes(content)
        children = [
            text_node_to_html_node(text_node)
            for text_node in children_text
            if text_node.text.strip()
        ]
        return ParentNode(tag=tag, children=children)

    if block_type == BlockDelimiters.CODE:
        code_content = "\n".join(block.split("\n")[1:-1])
        return ParentNode(
            tag="pre", children=[LeafNode(tag="code", value=code_content)]
        )

    if block_type == BlockDelimiters.QUOTE:
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

    if block_type == BlockDelimiters.UNORDERED_LIST:
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

    if block_type == BlockDelimiters.ORDERED_LIST:
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


def markdown_to_html_nodes(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    blocks_with_types = [(block, block_to_block_type(block)) for block in blocks]
    html_nodes = [
        block_to_html_nodes(block, block_type)
        for block, block_type in blocks_with_types
    ]

    parent_node = ParentNode(tag="div", children=html_nodes)
    return parent_node
