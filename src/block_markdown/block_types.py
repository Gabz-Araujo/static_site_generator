from typing import Callable
from html_node import HTMLNode

BlockTypeHandler = Callable[[str], bool]
BlockConverter = Callable[[str], HTMLNode]


class BlockDelimiters:
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
