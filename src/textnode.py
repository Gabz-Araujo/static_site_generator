from enum import Enum
from htmlnode import HTMLNode, LeafNode, PropsDict
from typing import Optional


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: str, url: Optional[str] = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    tag: Optional[str] = None
    value: Optional[str] = text_node.text
    props: Optional[PropsDict] = None
    text_type = None

    try:
        text_type = TextType[text_node.text_type.upper()]
    except KeyError:
        raise ValueError(f"Invalid text type: {text_node.text_type}")

    if text_type == TextType.TEXT:
        tag = None
    if text_type == TextType.BOLD:
        tag = "b"
    if text_type == TextType.ITALIC:
        tag = "i"
    if text_type == TextType.CODE:
        tag = "code"
    if text_type == TextType.LINK:
        tag = "a"
        if text_node.url:
            props = {"href": text_node.url}
    if text_type == TextType.IMAGE:
        tag = "img"
        value = ""
        if text_node.url:
            props = {"src": text_node.url, "alt": text_node.text}
    return LeafNode(value, tag, props=props)
