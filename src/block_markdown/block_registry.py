from typing import Dict
from .block_types import BlockTypeHandler, BlockConverter, BlockDelimiters
from html_node import HTMLNode, LeafNode, ParentNode


class BlockRegistry:
    def __init__(self):
        self.handlers: Dict[str, BlockTypeHandler] = {}
        self.converters: Dict[str, BlockConverter] = {}

    def register_block_type(
        self, name: str, handler: BlockTypeHandler, converter: BlockConverter
    ):
        self.handlers[name] = handler
        self.converters[name] = converter

    def detect_block_type(self, block: str) -> str:
        for name, handler in self.handlers.items():
            if handler(block):
                return name
        return BlockDelimiters.PARAGRAPH

    def convert_block(self, block: str, block_type: str) -> HTMLNode:
        if block_type in self.converters:
            return self.converters[block_type](block)
        return ParentNode(tag="p", children=[LeafNode(value=block)])
