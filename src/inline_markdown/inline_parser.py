from typing import List

from text_node import TextNode

from .inline_handlers import split_nodes_delimiter, split_nodes_image, split_nodes_link
from .inline_registry import InlineRegistry
from .inline_types import InlineDelimiters


def get_delimiters() -> List[str]:
    delimiters = []
    for dtype in InlineDelimiters:
        value = dtype.value
        if isinstance(value, tuple):
            delimiters.extend(value)
        elif value:
            delimiters.append(value)
    return delimiters


def create_delimiter_handler(delimiter: str):
    def handler(nodes: List[TextNode]) -> List[TextNode]:
        return split_nodes_delimiter(nodes, delimiter)

    return handler


def initialize_registry() -> InlineRegistry:
    registry = InlineRegistry()
    registry.register_handler("image", split_nodes_image)
    registry.register_handler("link", split_nodes_link)

    delimiters = get_delimiters()
    for delimiter in delimiters:
        registry.register_handler(
            f"delimiter_{delimiter}", create_delimiter_handler(delimiter)
        )

    return registry


def text_to_textnodes(text: str) -> List[TextNode]:
    registry = initialize_registry()
    return registry.process_text(text)
