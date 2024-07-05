from .block_registry import BlockRegistry
from .block_types import BlockDelimiters
from .block_handlers import (
    detect_paragraph,
    convert_paragraph,
    detect_heading,
    convert_heading,
    detect_code,
    convert_code,
    detect_quote,
    convert_quote,
    detect_unordered_list,
    convert_unordered_list,
    detect_ordered_list,
    convert_ordered_list,
)
from html_node import ParentNode
from .markdown_parser import markdown_to_blocks


def initialize_registry() -> BlockRegistry:
    registry = BlockRegistry()
    registry.register_block_type(
        BlockDelimiters.PARAGRAPH, detect_paragraph, convert_paragraph
    )
    registry.register_block_type(
        BlockDelimiters.HEADING, detect_heading, convert_heading
    )
    registry.register_block_type(BlockDelimiters.CODE, detect_code, convert_code)
    registry.register_block_type(BlockDelimiters.QUOTE, detect_quote, convert_quote)
    registry.register_block_type(
        BlockDelimiters.UNORDERED_LIST, detect_unordered_list, convert_unordered_list
    )
    registry.register_block_type(
        BlockDelimiters.ORDERED_LIST, detect_ordered_list, convert_ordered_list
    )
    return registry


def markdown_to_html_nodes(markdown: str) -> ParentNode:
    registry = initialize_registry()

    blocks = markdown_to_blocks(markdown)

    html_nodes = []

    for block in blocks:
        block_type = registry.detect_block_type(block)
        html_node = registry.convert_block(block, block_type)
        html_nodes.append(html_node)

    parent_node = ParentNode(tag="div", children=html_nodes)
    return parent_node
