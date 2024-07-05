from typing import Callable, Dict, List

from text_node import TextNode

InlineHandler = Callable[[List[TextNode]], List[TextNode]]


class InlineRegistry:
    def __init__(self):
        self.handlers: Dict[str, InlineHandler] = {}

    def register_handler(self, name: str, handler: InlineHandler):
        self.handlers[name] = handler

    def process_text(self, text: str) -> List[TextNode]:
        nodes = [TextNode(text, "text")]

        for _, handler in self.handlers.items():
            nodes = handler(nodes)

        return nodes
